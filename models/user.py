from config import TOKEN_LEN
from utils.ldap import authenticate_user
from utils.opt import random_string
from .db import db_main
from flask_login import UserMixin


class User(UserMixin, db_main.Model):
    __tablename__ = 'users'
    id = db_main.Column(db_main.Integer, primary_key=True)
    login = db_main.Column(db_main.String(255), unique=True)
    token = db_main.Column(db_main.String(TOKEN_LEN))
    role_id = db_main.Column(db_main.Integer)
    name = db_main.Column(db_main.String(255))
    email = db_main.Column(db_main.String(255))
    active = db_main.Column(db_main.Boolean, default=True)

    def __init__(self, login, name, email, active=1, role_id=2):
        self.login = login
        self.name = name
        self.email = email
        self.active = active
        self.token_generate()
        self.role_id = role_id

    def token_generate(self):
        self.token = random_string(TOKEN_LEN)

    def check_password(self, password):
        return authenticate_user(self.login, password)

    def check_token(self, token):
        return token == self.token

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def __repr__(self):
        return f'<User: {self.login} email: {self.email}>'
