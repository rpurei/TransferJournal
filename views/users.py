from config import LDAP_BIND_USER_NAME, LDAP_BIND_USER_PASSWORD, LDAP_SERVER_NAME, DEBUG, IMAGE_PATH
from app_logger import logger_output
from .forms import LoginPasswordForm, LoginTokenForm
from utils.ldap import authenticate_user, ldap_register
from utils.qrcode import make_qr
from models.user import User
from models.db import db_main
from flask import render_template, redirect, flash, url_for, Blueprint, abort
from flask_login import logout_user, current_user, login_user, login_required
from flask_login import LoginManager
from pathlib import Path

users_handler = Blueprint('users', __name__)
login_manager = LoginManager()


@login_required
@users_handler.route('/user/qr')
def user_home_qr():
    try:
        if current_user.is_authenticated:
            user_name = current_user.name
            qr_filename = f'{current_user.id}.png'
            qr_file = Path(IMAGE_PATH) / Path(qr_filename)    #'static/img/users/'
            if not qr_file.is_file():
                logger_output(f'File {qr_filename} not founded', DEBUG, 'error')
                abort(500, f'File {qr_filename} not founded')
            return render_template('qr.html', user_name=user_name, qr_filename=f'img/users/{qr_filename}')
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


@users_handler.route('/user/login-password', methods=['GET', 'POST'])
def auth_password_login():
    try:
        login_form = LoginPasswordForm()
        if login_form.validate_on_submit():
            user = User.query.filter_by(login=login_form.login.data).first()
            if user and user.active == 1:
                if authenticate_user(login_form.login.data, login_form.password.data):
                    login_user(user, remember=login_form.remember.data)
                    return redirect(url_for('users.user_home_qr'))
                else:
                    flash('Неверное имя пользователя/пароль !', 'danger')
                    logger_output(f'Login error: {login_form.data}', DEBUG, 'error')
            elif user and user.active == 0:
                flash('Пользователь отключен !', 'warning')
            else:
                register_result = ldap_register(LDAP_SERVER_NAME, LDAP_BIND_USER_NAME, LDAP_BIND_USER_PASSWORD,
                                                login_form.login.data)
                if register_result.get('status') == 'USER_FOUNDED':
                    try:
                        user = User(register_result.get('login'),
                                    register_result.get('full_name'),
                                    register_result.get('mail'))
                        db_main.session.add(user)
                        db_main.session.commit()
                        flash(f"""Пользователь {user.login} зарегистрирован""", 'success')
                        if make_qr(user.token, user.id) == 'error':
                            flash(f'Ошибка формирования QR кода, обратитесь в отдел РИПО', 'danger')
                        else:
                            if authenticate_user(login_form.login.data, login_form.password.data):
                                login_user(user, remember=login_form.remember.data)
                                return redirect(url_for('users.user_home_qr'))
                            else:
                                flash('Неверное имя пользователя/пароль !', 'danger')
                                logger_output(f'Login error: {login_form.data}', DEBUG, 'error')
                    except Exception as err:
                        logger_output(f'User registartion error: {str(err)}', DEBUG, 'error')
        return render_template('login_password.html', login_form=login_form)
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


@users_handler.route('/user/login-token', methods=['GET', 'POST'])
def auth_token_login():
    try:
        login_form = LoginTokenForm()
        if login_form.validate_on_submit():
            user = User.query.filter_by(token=login_form.token.data).first()
            if user and user.active == 1:
                login_user(user, remember=login_form.remember.data)
                return redirect(url_for('index.get_index'))
            elif user and user.active == 0:
                flash('Пользователь отключен !', 'warning')
            else:
                flash('Пользователь с указанным токеном не найден !', 'danger')
                logger_output(f'Login error: {login_form.data}', DEBUG, 'error')
        return render_template('login_token.html', login_form=login_form)
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
        abort(500, str(err))


@users_handler.route('/user/logout')
def auth_logout():
    logout_user()
    return redirect(url_for('index.get_index'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash(f'Авторизуйтесь для доступа к странице', 'warning')
    return redirect(url_for('users.auth_token_login'))
