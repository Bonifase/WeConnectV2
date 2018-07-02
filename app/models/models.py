from app import db, app
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.check_pattern import *


class User(db.Model):
    """This class defines the users table """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column("username", db.String(80))
    _email = db.Column("email", db.String(120), unique=True)
    _password = db.Column("password", db.String(80))
    businesses = db.relationship('Business', backref='owner', lazy='dynamic')
    reviews = db.relationship('Review', backref='owner', lazy='dynamic')

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def reset_password(self, new_password):
        self.password = new_password

    def register_user(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    """defines username attribute for user object"""
    @hybrid_property
    def username(self):
        return self._username
    """validates with predefined patterns"""
    @username.setter
    def username(self, value):
        match = name_pattern(value)
        if match:
            self._username = value
            return
        assert 0, 'Invalid username'

    """defines an email attribute for user object"""
    @hybrid_property
    def email(self):
        return self._email

    """validates with predefined patterns and sets 
    an email attribute for user object"""
    @email.setter
    def email(self, value):
        match = email_pattern(value)
        if match:
            self._email = value
            return
        assert 0, 'Invalid email'

    """defines password attribute for user object"""
    @hybrid_property
    def password(self):
        return self._password

    """validates with predefined patterns and sets 
    password attribute for user object"""
    @password.setter
    def password(self, value):
        match = password_pattern(value)
        if match:
            self._password = Bcrypt().generate_password_hash(value).decode()
            return
        assert 0, 'Password should contain numbers and characters'

    """defines new password attribute"""
    @hybrid_property
    def new_password(self):
        return self._password

    """validates with predefined patterns and sets 
    a new password attribute for user object"""
    @new_password.setter
    def new_password(self, value):
      
        match = password_pattern(value)

        if match:
            self._password = value
            return

        assert 0, 'Invalid new password'


class Business(db.Model):
    """This class defines the businesses table."""

    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column("name", db.String(80), unique=True)
    _category = db.Column("category", db.String(120))
    _location = db.Column("location", db.String(80))
    description = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE', onupdate='CASCADE'))
    reviews = db.relationship('Review', backref='reviewowner', lazy='dynamic') 
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name, category, location, description, userid):
        self.name = name
        self.category = category
        self.location = location
        self.description = description
        self.userid = userid
    """method that updates the business"""

    def update_business(self, data, issuer_id):
        # data  is a dictionary
        if issuer_id == self.userid:
            for key in data.keys():
                value = data[key]
                setattr(self, key, value)
                db.session.add(self)
                db.session.commit()
        else:
            assert 0, 'This business is registered to another user'

    """method that saves the business to the database"""
    def save_business(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def businesses():
        businesses = Business.query.all()
        return businesses

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @hybrid_property
    def name(self):
        return self._name

    """sets the name of the business attribute"""
    @name.setter
    def name(self, value):       
        match = name_pattern(value)
        if match:
            self._name = value
            return
        assert 0, 'Invalid name'

    @hybrid_property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):       
        match = attribute_pattern(value)
        if match:
            self._category = value
            return
        assert 0, 'Invalid category'

    @hybrid_property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):      
        match = attribute_pattern(value)
        if match:
            self._location = value
            return
        assert 0, 'Invalid location'


class Review(db.Model):
    """This class defines the reviews table."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    _reviewbody = db.Column("reviewbody", db.String(80))
    businessid = db.Column(db.Integer, db.ForeignKey(
        'businesses.id', ondelete="CASCADE", onupdate="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, reviewbody, businessid, user_id):
        self._reviewbody = reviewbody
        self.businessid = businessid
        self.user_id = user_id

    @staticmethod
    def reviews():
        reviews = Review.query.all()
        return reviews

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @hybrid_property
    def reviewbody(self):
        return self._reviewbody

    @reviewbody.setter
    def reviewbody(self, value):      
        match = attribute_pattern(value)
        if match:
            self._reviewbody = value
            return
        assert 0, 'Invalid category'      
