from flask import Flask

import json, jwt, datetime
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)	

from app import views