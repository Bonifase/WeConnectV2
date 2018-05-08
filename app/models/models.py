import re
from app import db
from flask_bcrypt import Bcrypt


class User(db.Model):
    """This class defines the users table """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column("username", db.String(80))
    _email = db.Column("email", db.String(120), unique=True)
    _password = db.Column("password", db.String(80))
    businesses = db.relationship('Business', backref = 'owner', lazy = 'dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def reset_password(self, newpassword):
        self.password = newpassword

    def register_user(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        pattern = r'[a-zA-Z]{3,8}'
        match = re.search(pattern, value)
        if match:
            self._username = value
            return
        assert 0, 'Invalid username'

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = r'[a-zA-Z0-9_\.&-]{4,30}@[a-z]+\..'
        match = re.search(pattern, value)
        if match:
            self._email = value
            return
        assert 0, 'Invalid email'

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        pattern = r'[a-zA-Z0-9_@&\.]{6,20}'
        match = re.search(pattern, value)
        if match:
            self._password = value
            return
        assert 0, 'Invalid password'

    @property
    def newpassword(self):
        return self._password

    @newpassword.setter
    def newpassword(self, value):
        pattern = r'[a-zA-Z0-9_@&\.]{6,20}'
        match = re.search(pattern, value)

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
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref = 'reviewowner', lazy = 'dynamic') 
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
   
    def __init__(self, name, category, location,description):
        self.name = name
        self.category = category
        self.location = location
        self.description = description
    
    def update_business(self, data, issuer_id):
        # data  is a dict
        if issuer_id == self.userid:
            for key in data.keys():
                value = data[key]
                setattr(self, key, value)
        else:
            assert 0, 'This business is registered to another user'

    def save_business(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Business.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        pattern = r'[a-zA-Z\. ]{3,10}'
        match = re.search(pattern, value)
        if match:
            self._name = value
            return
        assert 0, 'Invalid name'

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        pattern = r'[a-zA-Z\. ]{1,15}'
        match = re.search(pattern, value)
        if match:
            self._category = value
            return
        assert 0, 'Invalid category'

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        pattern = r'[a-zA-Z\. ]{3,10}'
        match = re.search(pattern, value)
        if match:
            self._location= value
            return
        assert 0, 'Invalid location'

class Review(db.Model):
    """This class defines the reviews table."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    reviewbody = db.Column(db.Text)
    businessid = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    
    def __init__(self, reviewbody, businessid):
        self.reviewbody = reviewbody
        self.businessid = businessid
        

        
