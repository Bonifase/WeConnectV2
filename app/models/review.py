import re
from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewbody = db.Column(db.Text)
    businessid = db.Column(db.Integer, db.ForeignKey('business.id'))
    
    class_counter= 1
    def __init__(self, reviewbody, businessid):
        self.reviewbody = reviewbody
        self.businessid = businessid
        self.id= Review.class_counter
        Review.class_counter += 1
        
