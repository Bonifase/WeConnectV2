import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app

# app = Flask(__name__)
# app.config['SECRET_KEY'] = "Thisismysecretkey"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:boni@orwa@localhost/weconnect"
db = SQLAlchemy(app)

"""initialize migrate"""
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    """This class defines the users table """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    businesses = db.relationship(
        'Business', primaryjoin="and_(User.id==Business.userid )")
    reviews = db.relationship(
        'Review', primaryjoin="and_(User.id==Review.user_id )")


class Business(db.Model):
    """This class defines the businesses table."""

    __tablename__ = 'businesses'

    __searchable__ = ['name', 'category', 'location']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    category = db.Column(db.String(120))
    location = db.Column(db.String(80))
    description = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship(
        'Review', primaryjoin="and_(Business.id==Review.businessid )")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    reviewbody = db.Column(db.String(100))
    businessid = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
