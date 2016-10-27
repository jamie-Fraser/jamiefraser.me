import os
from flask import Flask, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy
from flask_login import LoginManager
from config import basedir
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.create_all()

bcrypt = Bcrypt(app)

from app import views, models