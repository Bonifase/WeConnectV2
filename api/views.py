from app import app
from models.models import *
from flask import request,make_response, jsonify
import json, jwt, datetime


#Endpoint to Register user and ssaving the details in a list called users
@app.route('/api/v2/auth/register',  methods = ['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    #check if the user details already in the list, otherwise add the details in the list
    users = User.query.all()
    available_emails = [x.email for x in users]
    if email in available_emails:
        return make_response(jsonify({"status": "Conflict", "message": "User Details Exist"}), 409)
    else:
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
    return make_response(jsonify({"status": "ok", "message": "Registered Successful"}), 201)

#Login user
@app.route('/api/v2/auth/login',  methods = ['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #check if the user details exist in the list, otherwise deny access.
    users = User.query.all()
    user = [x for x in users if x.username == username]
    if user:
        if password == user[0].password:
            return make_response(jsonify({"status": "ok", "message": "Login Successful"}), 200)

        else:
            return make_response(jsonify({"status": "Conflict", "message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({"status": "Conflict", "message": "Wrong Login Details"}), 409)
   
#Reset password
@app.route('/api/v2/auth/reset-password', methods = ['POST'])
def reset_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    resetpassword = data['resetpassword']
    users = User.query.all()
    user = [x for x in users if x.username == username]
    if user and password == user[0].password:
        user[0].password = resetpassword
        db.session.commit()
        return make_response(jsonify({"status": "Created", "message": "Reset Successful"}), 201)
       
    else:
        return make_response(jsonify({"status": "Conflict", "message": "Type Different Password"}), 409)
#Logout User
@app.route('/api/v2/auth/logout', methods = ['POST'])
def logout():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #check if the user details exist in the list, otherwise deny access.
    users = User.query.all()
    user = [x for x in users if x.username == username]
    if user:
        if password == user[0].password:
            return make_response(jsonify({"status": "ok", "message": "Logout Successful"}), 200)

        else:
            return make_response(jsonify({"status": "Conflict", "message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({"status": "Conflict", "message": "Wrong Login Details"}), 409)


#Create new business
@app.route('/api/v2/auth/businesses', methods = ['POST'])
def create_business():
    data = request.get_json()
    name = data["name"]
    category = data["category"]
    location = data["location"]
    description = data["description"]
     #check if the business details already in the list, otherwise create the object in the list
    businesses = Business.query.all()
    available_names = [x.name for x in businesses]
    if name in available_names:
        return make_response(jsonify({"status": "Conflict", "message": "Business already Exist, use another name"}), 409)
    else:
        business = Business(name, category, location, description)
        businesses.append(business)
        myresponse = {'name':business.name, 'category':business.category, 'location':business.location, 'description':business.description}
    return make_response(jsonify(myresponse), 201)

#Get all the businesses
@app.route('/api/v2/auth/businesses', methods = ['GET'])
def view_businesses():
    businesses = Business.query.all()
    mybusinesses = [{x.id : [x.name, x.category, x.location] for x in businesses}]
    return make_response(jsonify({"status": "ok", "message": "Available Businesses", "businesses":mybusinesses}), 200)

#Get a business by id
@app.route('/api/v2/auth/business/<int:id>/')
def get_business(id):
    mybusiness = [x for x in businesses if x.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        return  make_response(jsonify({"status": "ok", "message": "Available Business", "business":{'name':mybusiness.name, 'category':mybusiness.category, 'location':mybusiness.location, 'description':mybusiness.description}}), 200)
    else:
         return  make_response(jsonify({"status": "not found", "message": "No such Businesses",}), 404)

#Update business
@app.route('/api/v2/auth/business/<int:id>/', methods = ['PUT'])
def update_business(id):
    data = request.get_json()
    newname = data["name"]
    newcategory = data["category"]
    newlocation = data["location"]
    newdescription = data["description"]
    mybusiness = [x for x in businesses if x.id == id]
    if mybusiness:
        mybusiness[0].update_business(newname, newcategory, newlocation, newdescription)
        return  make_response(jsonify({"status": "Created", "message": "Business Updated",}), 201)
    else:
         return  make_response(jsonify({"status": "not found", "message": "No such Businesses",}), 404)

#Delete business
@app.route('/api/v2/auth/business/<int:id>/', methods = ['DELETE'])
def delete_business(id):
    mybusiness = [x for x in businesses if x.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        businesses.remove(mybusiness)
        return  make_response(jsonify({"status": "Created", "message": "Business deleted",}), 201)
    else:
         return  make_response(jsonify({"status": "not found", "message": "No such Businesses",}), 404)

#Add a review for a business
@app.route('/api/v2/auth/<int:businessid>/reviews', methods = ['POST'])
def reviews(businessid):
    data = request.get_json()
    reviewbody = data["reviewbody"]
    businessid = data['businessid']
     #check if the review details already in the list, otherwise create the review object in the list
    business_reviews = Review.query.all()
    available_reviewbodies = [x.reviewbody for x in business_reviews ]
    if reviewbody in available_reviewbodies:
        return make_response(jsonify({"status": "Conflict", "message": "Review already Exist, use another description"}), 409)
    else:
        business_review = Review(reviewbody, businessid)
        db.session.add(business_review)
        db.session.commit()
    return make_response(jsonify({"status": "CREATED", "message": "Review added Successfully"}), 201)

#Get all reviews for a business
@app.route('/api/v2/auth/<int:businessid>/reviews', methods = ['GET'])
def myreviews(businessid):
    business_reviews = Review.query.all()
    myreviews = [{x.id : [x.businessid, x.reviewbody] for x in business_reviews}]
    return make_response(jsonify({"status": "ok", "message": "Available reviews", "Reviews":myreviews}), 200)

