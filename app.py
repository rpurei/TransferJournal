from app_logger import logger_output
from config import DEBUG, IMAGE_PATH
from views import views_handler
from views.users import users_handler, login_manager
from views.index import index_handler
from views.docs import docs_handler
from models.db import db_main
from flask import Flask
from pathlib import Path


def create_app():
    try:
        app = Flask(__name__)
        app.config.from_pyfile('config.py')
        db_main.init_app(app)
        login_manager.init_app(app)
        app.register_blueprint(index_handler)
        app.register_blueprint(users_handler)
        app.register_blueprint(views_handler)
        app.register_blueprint(docs_handler)
        return app
    except Exception as err:
        logger_output(str(err), DEBUG, 'error')
