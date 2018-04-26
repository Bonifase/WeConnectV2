from flask import Flask, request, jsonify, make_response
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisismysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:boni@orwa@localhost/weconnect"

db = SQLAlchemy(app)


from views import *



if __name__ == '__main__':

    app.run(debug=True)