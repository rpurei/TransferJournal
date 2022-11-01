from app_logger import logger_output
from config import LDAP_BASE_DN, LDAP_SERVER_NAME, DEBUG
import ldap


def ldap_register(address, bind_username, bind_password, user_login):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    basedn = LDAP_BASE_DN
    search_filter = f'(&(objectCategory=person)(objectClass=user)(mail={user_login}))'
    search_attribute = ['mail', 'cn']
    search_scope = ldap.SCOPE_SUBTREE
    register_result = {'status': '', 'login': '', 'mail': '', 'full_name': ''}
    try:
        result = conn.simple_bind_s(bind_username, bind_password)
        try:
            ldap_result_id = conn.search(basedn, search_scope, search_filter, search_attribute)
            while 1:
                result_type, result_data = conn.result(ldap_result_id, 0)
                if not result_data:
                    register_result['status'] = 'USER_NOT_FOUNDED'
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        register_result['full_name'] = result_data[0][1]['cn'][0].decode('utf-8')
                        register_result['login'] = user_login
                        register_result['mail'] = result_data[0][1]['mail'][0].decode('utf-8')
            if len(register_result['login']) > 0:
                register_result['status'] = 'USER_FOUNDED'
        except ldap.LDAPError as err:
            logger_output(str(err), DEBUG, 'error')
    except ldap.INVALID_CREDENTIALS:
        register_result['status'] = 'LDAP_SRV_INVALID_CRED'
    except ldap.SERVER_DOWN:
        register_result['status'] = 'LDAP_SRV_UNREACH'
    except ldap.LDAPError as e:
        register_result['status'] = f'LDAP_OTHER_ERROR: {str(e)}'
    finally:
        conn.unbind_s()
    return register_result


def ldap_auth(address, bind_username, bind_password):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    register_result = {'status': ''}
    try:
        result = conn.simple_bind_s(bind_username, bind_password)
        register_result['status'] = 'USER_AUTHENTICATED'
        register_result['username'] = bind_username
    except ldap.INVALID_CREDENTIALS:
        register_result['status'] = 'LDAP_SRV_INVALID_CRED'
    except ldap.SERVER_DOWN:
        register_result['status'] = 'LDAP_SRV_UNREACH'
    except ldap.LDAPError as e:
        register_result['status'] = f'LDAP_OTHER_ERROR: {str(e)}'
    finally:
        conn.unbind_s()
    return register_result


def authenticate_user(username, password):
    result = ldap_auth(LDAP_SERVER_NAME, username, password)
    return True if result['status'] == 'USER_AUTHENTICATED' else False
