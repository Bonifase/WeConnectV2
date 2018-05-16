from flask import Flask

import json, jwt, datetime
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'supersecretishere'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)



from app import views