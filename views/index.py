from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import current_user


index_handler = Blueprint('index', __name__)


@index_handler.route('/')
def get_index():
    if current_user.is_authenticated:
        user_name = current_user.name
        return render_template('index.html', user_name=user_name)
    else:
        return redirect(url_for('users.auth_token_login'))
