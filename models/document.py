from config import DIRECTUM_PAGE_ID_LEN, TRANSACTION_ID_LEN
from .db import db_main
from sqlalchemy.sql import func


class DocumentStatus(db_main.Model):
    __tablename__ = 'docs_statuses'
    id = db_main.Column(db_main.Integer, primary_key=True)
    login = db_main.Column(db_main.String(255))
    directum_paper_id = db_main.Column(db_main.String(DIRECTUM_PAGE_ID_LEN))
    operation = db_main.Column(db_main.String(255))
    created = db_main.Column(db_main.DateTime(timezone=True), server_default=func.now())

    def __init__(self, login, directum_paper_id, operation):
        self.login = login
        self.directum_paper_id = directum_paper_id
        self.operation = operation


class DocumentTransaction(db_main.Model):
    __tablename__ = 'docs_transactions'
    id = db_main.Column(db_main.Integer, primary_key=True)
    login = db_main.Column(db_main.String(255))
    transaction_id = db_main.Column(db_main.String(TRANSACTION_ID_LEN))
    directum_paper_id = db_main.Column(db_main.String(DIRECTUM_PAGE_ID_LEN))
    created = db_main.Column(db_main.DateTime(timezone=True), server_default=func.now())

    def __init__(self, login, transaction_id, directum_paper_id):
        self.login = login
        self.transaction_id = transaction_id
        self.directum_paper_id = directum_paper_id


class DocumentContent(db_main.Model):
    __tablename__ = 'docs_contents'
    id = db_main.Column(db_main.Integer, primary_key=True)
    directum_paper_id = db_main.Column(db_main.String(DIRECTUM_PAGE_ID_LEN))
    directum_name = db_main.Column(db_main.String(255))
    directum_id = db_main.Column(db_main.Integer)
    created = db_main.Column(db_main.DateTime(timezone=True), server_default=func.now())

    def __init__(self, directum_paper_id, directum_name, directum_id):
        self.directum_paper_id = directum_paper_id
        self.directum_name = directum_name
        self.directum_id = directum_id
