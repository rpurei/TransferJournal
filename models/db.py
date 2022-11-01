from config import SQLALCHEMY_DATABASE_URI
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

db_main = SQLAlchemy()
database_engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
