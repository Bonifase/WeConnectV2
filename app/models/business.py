import re
from app import db

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

    @classmethod
    def register_business(cls, name, category, location, description):
        business = cls()
        business.name = name
        business.category = category
        business.location = location
        business.description = description
        business.id = Business.class_counter
        cls.businesses.append(business)
        Business.class_counter += 1
        return business

    def __init__(self, name=None, category=None, location=None, description=None):
        self._name = name
        self._category = category
        self._location = location

    def update_business(self, newname, newcategory, newlocation, newdescription):
        self.name = newname
        self.category = newcategory
        self.location = newlocation
        self.description = newdescription

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
    def newname(self):
        return self._name

    @newname.setter
    def newname(self, value):
        pattern = r'[a-zA-Z\. ]{3,10}'
        match = re.search(pattern, value)
        if match:
            self._name = value
            return
        assert 0, 'Invalid name' 
