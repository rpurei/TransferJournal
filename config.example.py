TESTING = True
DEBUG = True
ENV = 'development'

APP_PORT = 3000
APP_HOST = 'localhost'
APP_ITEMS_PER_PAGE = 5

LOG_FOLDER = 'logs'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
LOG_FILE = 'app.log'
LOG_MAX_BYTES = 1048576
LOG_COUNT = 10

DB_HOST = '172.16.0.179'
DB_NAME = 'db_transferjournal_dev'
DB_PORT = ''
DB_USER = 'dbu_journal'
DB_PASSWORD = 'vHbg8v7s6df45ZDe46'

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8'

IMAGE_PATH = 'static/img/users/'

SECRET_KEY = 'b49e3d63dd7da4eb7a408ca23f7ac3cd8013d485d40d1b6941662213a85a3d81'

LDAP_BASE_DN = 'dc=gkzd,dc=local'
LDAP_SERVER_NAME = 'bl-dc1.gkzd.local'
LDAP_BIND_USER_NAME = 'webappusr@zdmail.ru'
LDAP_BIND_USER_PASSWORD = '403u&O5avI'

TEMP_DIR = 'tmp'
TEMP_NAME_LENGTH = 16

TOKEN_LEN = 128
TRANSACTION_ID_LEN = 64

DIRECTUM_PAGE_ID_LEN = 32
DIRECTUM_API_USER = 'integration'
DIRECTUM_API_PASSWORD = 'Lih15H1O6TikjJgeM4hE1exn'
DIRECTUM_PROTOCOL = 'http://'                       #'https://'
DIRECTUM_URL = '172.16.0.191'                       # contract.zdmail.ru
DIRECTUM_API_URL = '/DrxIntegrationLocal/odata'     # /DrxIntegration/odata
DIRECTUM_GET_DOC_BY_QR = '/CustomAPI/GetDocByQR'
DIRECTUM_SET_DOC_PAPER_OPERATION = '/CustomAPI/SetDocPaperOperation'

OPERATION_SEND_NAME = 'Документ передан'
OPERATION_ACCEPT_NAME = 'Документ принят'
