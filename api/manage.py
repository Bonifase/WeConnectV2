from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisismysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:boni@orwa@localhost/weconnect"
db = SQLAlchemy(app)


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    businesses = db.relationship('Business', backref = 'owner', lazy = 'dynamic')

class Business(db.Model):
    __searchable__ = ['name', 'category', 'location']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    category = db.Column(db.String(120))
    location = db.Column(db.String(80))
    description = db.Column(db.Text)
    ownerid = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviews = db.relationship('Review', backref = 'reviewowner', lazy = 'dynamic') 
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewbody = db.Column(db.Text)
    businessid = db.Column(db.Integer, db.ForeignKey('business.id'))


if __name__ == '__main__':
    manager.run()
