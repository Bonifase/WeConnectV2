from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    businesses = db.relationship('Business', backref = 'owner', lazy = 'dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def reset_password(self, resetpassword):
        self.password = resetpassword


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    category = db.Column(db.String(120))
    location = db.Column(db.String(80))
    description = db.Column(db.Text)
    ownerid = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviews = db.relationship('Review', backref = 'reviewowner', lazy = 'dynamic') 
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
   
    def __init__(self, name, category, location,description):
        self.name = name
        self.category = category
        self.location = location
        self.description = description
    
    def update_business(self,newname, newcategory, newlocation, newdescription):
        self.name = newname
        self.category = newcategory
        self.location = newlocation
        self.description = newdescription

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Business.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewbody = db.Column(db.Text)
    businessid = db.Column(db.Integer, db.ForeignKey('business.id'))
    
    def __init__(self, reviewbody, businessid):
        self.reviewbody = reviewbody
        self.businessid = businessid
        
        