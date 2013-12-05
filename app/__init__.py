from flask import Flask
from werkzeug import Local, LocalProxy

from models.database import db_session, Base

app = Flask(__name__)
l = Local()
l.session = db_session


from app import views

