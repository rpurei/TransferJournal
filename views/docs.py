from config import (DEBUG, TRANSACTION_ID_LEN,
                    OPERATION_SEND_NAME, OPERATION_ACCEPT_NAME,
                    DIRECTUM_API_USER, DIRECTUM_API_PASSWORD,
                    DIRECTUM_PROTOCOL, DIRECTUM_URL, DIRECTUM_API_URL,
                    DIRECTUM_GET_DOC_BY_QR, DIRECTUM_SET_DOC_PAPER_OPERATION,
                    APP_ITEMS_PER_PAGE)
from models.db import db_main
from models.document import DocumentTransaction, DocumentStatus, DocumentContent
from models.user import User
from utils.opt import random_string
from app_logger import logger_output
from flask import render_template, redirect, url_for, request, Blueprint, abort
from flask_login import current_user
import requests
import json
from datetime import datetime

docs_handler = Blueprint('docs', __name__)

directum_headers = {'Username': DIRECTUM_API_USER,
                    'Password': DIRECTUM_API_PASSWORD,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Return': 'representation',
                    'Culture': 'ru-RU'}

get_doc_by_qr_uri = (DIRECTUM_PROTOCOL +
                     DIRECTUM_URL +
                     DIRECTUM_API_URL +
                     DIRECTUM_GET_DOC_BY_QR)

post_doc_paper_operation = (DIRECTUM_PROTOCOL +
                            DIRECTUM_URL +
                            DIRECTUM_API_URL +
                            DIRECTUM_SET_DOC_PAPER_OPERATION)


@docs_handler.route('/docs/send')
def docs_send():
    try:
        if current_user.is_authenticated:
            user_name = current_user.name
            return render_template('send.html', user_name=user_name)
        else:
            return redirect(url_for('users.auth_token_login'))
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


@docs_handler.route('/docs/accept')
def docs_accept():
    try:
        if current_user.is_authenticated:
            user_name = current_user.name
            return render_template('accept.html', user_name=user_name)
        else:
            return redirect(url_for('users.auth_token_login'))
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


def docs_operation_processor(request_data, operation_message):
    try:
        for form_id, qr_code in request_data.items():
            if form_id.startswith('input-qr-code-'):
                doc_content = DocumentStatus(current_user.login,
                                             qr_code,
                                             operation_message)
                db_main.session.add(doc_content)
                db_main.session.commit()
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


def docs_directum_processor(doc_qr_code, user_name, operation_id):
    try:
        response_directum_get_qr = requests.get(get_doc_by_qr_uri + f"(docQR='{doc_qr_code}')", headers=directum_headers)
        print(get_doc_by_qr_uri + f"(docQR='{doc_qr_code}')")
        if response_directum_get_qr.status_code == 200:
            get_qr_json = response_directum_get_qr.json()
            get_qr_value = dict(get_qr_json).get('value')
            if len(get_qr_value) > 2:
                get_qr_dict = json.loads(get_qr_value)
                doc_content = DocumentContent(doc_qr_code,
                                              get_qr_dict['name'],
                                              get_qr_dict['id'])
                db_main.session.add(doc_content)
                db_main.session.commit()
            else:
                error_message = f'Requested QR: {doc_qr_code} not founded in Directum'
                logger_output(error_message, DEBUG, 'error')
                abort(404, error_message)
        elif response_directum_get_qr.status_code == 404:
            error_message = f'Error 404 processing request to API URL: {get_doc_by_qr_uri}(docQR="{doc_qr_code}")'
            logger_output(error_message, DEBUG, 'error')
            abort(404, error_message)
        else:
            error_message = f'GET to /GetDocByQR error code: {response_directum_get_qr.status_code}'
            logger_output(error_message, DEBUG, 'error')
            abort(400, error_message)
        payload_directum = {'docQR': f'{doc_qr_code}',
                            'userFIO': f'{user_name}',
                            'docOperationCode': operation_id}
        response_directum_set_doc_operation = requests.post(post_doc_paper_operation,
                                                            data=json.dumps(payload_directum),
                                                            headers=directum_headers)
        if response_directum_set_doc_operation.status_code != 204:
            error_message = f'POST to /SetDocPaperOperation error code: {response_directum_set_doc_operation.status_code} {response_directum_set_doc_operation.text}'
            logger_output(error_message, DEBUG, 'error')
            abort(400, error_message)
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


@docs_handler.route('/docs/send/processing', methods=['POST'])
def docs_send_processing():
    try:
        if current_user.is_authenticated:
            if request.method == 'POST':
                request_data = request.form.to_dict()
                transaction_id = random_string(TRANSACTION_ID_LEN)
                docs_operation_processor(request_data, OPERATION_SEND_NAME)
                for form_id, qr_code in request_data.items():
                    if form_id.startswith('input-qr-code-') and len(qr_code) > 0:
                        doc_transaction = DocumentTransaction(current_user.login, transaction_id, qr_code)
                        db_main.session.add(doc_transaction)
                        db_main.session.commit()
                        docs_directum_processor(qr_code, current_user.name, 0)
                return redirect(url_for('docs.docs_send'))
        else:
            return redirect(url_for('users.auth_token_login'))
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


@docs_handler.route('/docs/accept/processing', methods=['POST'])
def docs_accept_processing():
    try:
        if current_user.is_authenticated:
            if request.method == 'POST':
                request_data = request.form.to_dict()
                docs_operation_processor(request_data, OPERATION_ACCEPT_NAME)
                for form_id, qr_code in request_data.items():
                    if form_id.startswith('input-qr-code-') and len(qr_code) > 0:
                        docs_directum_processor(qr_code, current_user.name, 1)
                return redirect(url_for('docs.docs_accept'))
        else:
            return redirect(url_for('users.auth_token_login'))
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


@docs_handler.route('/docs/search', methods=['GET'])
def docs_search_action():
    if current_user.is_authenticated:
        user_name = current_user.name
        page = request.args.get('page', type=int, default=1)
        search_string = request.args.get('search_string')
        current_year = datetime.now().year
        start_date = request.args.get('start_date', f'{current_year}-01-01')
        end_date = request.args.get('end_date', f'{current_year}-12-31')
        start_date = start_date if start_date != '' else f'{current_year}-01-01'
        if end_date != '' and not end_date.endswith('23:59:59'):
            end_date = end_date + ' 23:59:59'
        elif end_date != '' and end_date.endswith('23:59:59'):
            pass
        else:
            end_date = f'{current_year}-12-31'
        doc_directum_paper_ids = db_main.session.query(User.name,
                                             DocumentStatus.operation,
                                             DocumentStatus.created,
                                             DocumentStatus.directum_paper_id,
                                             DocumentContent.directum_id,
                                             DocumentContent.directum_name).join(User,
                                                                                 DocumentStatus.login == User.login).join(DocumentContent, DocumentStatus.directum_paper_id == DocumentContent.directum_paper_id).filter(DocumentStatus.directum_paper_id.like(search_string),
                                                                                                                          DocumentStatus.created >= start_date,
                                                                                                                          DocumentStatus.created <= end_date).order_by(DocumentStatus.created).group_by(User.name,
                                                                                                                                                                                                        DocumentStatus.operation,
                                                                                                                                                                                                        DocumentStatus.created,
                                                                                                                                                                                                        DocumentStatus.directum_paper_id,
                                                                                                                                                                                                        DocumentContent.directum_id,
                                                                                                                                                                                                        DocumentContent.directum_name)
        doc_directum_paper_ids = doc_directum_paper_ids if doc_directum_paper_ids.count() > 0 else None
        doc_directum_names = db_main.session.query(User.name,
                                             DocumentStatus.operation,
                                             DocumentStatus.created,
                                             DocumentStatus.directum_paper_id,
                                             DocumentContent.directum_id,
                                             DocumentContent.directum_name).join(User,
                                                                                 DocumentStatus.login == User.login).join(DocumentContent, DocumentStatus.directum_paper_id == DocumentContent.directum_paper_id).filter(
                                                                                                                          DocumentContent.directum_name.like(f'%{search_string}%'),
                                                                                                                          DocumentStatus.created >= start_date,
                                                                                                                          DocumentStatus.created <= end_date).order_by(DocumentStatus.created).group_by(User.name,
                                                                                                                                                                                                        DocumentStatus.operation,
                                                                                                                                                                                                        DocumentStatus.created,
                                                                                                                                                                                                        DocumentStatus.directum_paper_id,
                                                                                                                                                                                                        DocumentContent.directum_id,
                                                                                                                                                                                                        DocumentContent.directum_name).paginate(page=page, per_page=APP_ITEMS_PER_PAGE, error_out=False, count=True)
        doc_directum_names = doc_directum_names if len([page for page in doc_directum_names.iter_pages()]) else None
        doc_directum_ids = db_main.session.query(User.name,
                                                 DocumentStatus.operation,
                                                 DocumentStatus.created,
                                                 DocumentStatus.directum_paper_id,
                                                 DocumentContent.directum_id,
                                                 DocumentContent.directum_name).join(User,
                                                                                     DocumentStatus.login == User.login).join(DocumentContent, DocumentStatus.directum_paper_id == DocumentContent.directum_paper_id).filter(
                                                                                                                                DocumentContent.directum_id == search_string,
                                                                                                                                DocumentStatus.created >= start_date,
                                                                                                                                DocumentStatus.created <= end_date).order_by(DocumentStatus.created).group_by(User.name,
                                                                                                                                                                                                              DocumentStatus.operation,
                                                                                                                                                                                                              DocumentStatus.created,
                                                                                                                                                                                                              DocumentStatus.directum_paper_id,
                                                                                                                                                                                                              DocumentContent.directum_id,
                                                                                                                                                                                                              DocumentContent.directum_name)
        doc_directum_ids = doc_directum_ids if doc_directum_ids.count() > 0 else None
        if end_date.endswith('23:59:59'):
            end_date = end_date.replace(' 23:59:59', '')
        return render_template('index.html',
                               user_name=user_name,
                               doc_directum_paper_ids=doc_directum_paper_ids,
                               doc_directum_names=doc_directum_names,
                               doc_directum_ids=doc_directum_ids,
                               start_date=start_date,
                               end_date=end_date,
                               search_string=search_string
                               )
    else:
        return redirect(url_for('users.auth_token_login'))


@docs_handler.route('/docs/search/result', methods=['POST'])
def docs_search_result():
    pass
