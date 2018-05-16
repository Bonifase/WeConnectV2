from flask import request, jsonify, make_response, session, logging
from functools import wraps
from  flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from app.errorhandler import *
from jwt.exceptions import InvalidTokenError

from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt, decode_token
)

from app import app
bcrypt = Bcrypt(app)
from .models import *

from app.helpers import clean_data
from app.helpers import *
jwt = JWTManager(app)
blacklist = set()
stored_reset_tokens = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/')
def index():
    return jsonify("Welcome To WeConnect")

# Endpoint to Register user and ssaving the details in a list called users


@register_user()
def register_user():

    data = request.get_json()
    
    user = {'username':data.get('username'), 'email' : data.get('email'), 'password':data.get('password')}
    try:
        cleaned_data = clean_data(**user)
    except AssertionError as error:
        return jsonify({'error': error.args[0]}), 409

    if cleaned_data:
    
        users = User.query.all()
        available_emails = [user.email for user in users]

        if data.get('email') in available_emails:
            return make_response(jsonify({"message": "User already exists. Please login"}), 409)
        
        else:
            try:
                user = User(cleaned_data['username'], cleaned_data['email'], cleaned_data['password'])
                user.register_user()
            except AssertionError as err:
                return make_response(jsonify({'error': err.args[0]}), 409)

        return make_response(jsonify({"message": "You registered successfully. Please log in"}), 201)

    # Login user

@login()
def login():

    data = request.get_json()
    user = {'email' : data.get('email'), 'password':data.get('password')}

    try:
        cleaned_data = clean_data(**user)
    except AssertionError as error:
        return jsonify({'error': error.args[0]}), 409

    if cleaned_data:
    #Get all user from datbase    

        user = User.query.filter_by(email=cleaned_data["email"]).first()
        if user:
            if Bcrypt().check_password_hash(user.password, cleaned_data["password"]):
    
                access_token = create_access_token(identity=user.id)
                           
                if access_token:
                    response = {
                                'message': 'You logged in successfully.',
                                'access_token': access_token
                            }
                return jsonify(response), 200

            else:
                return jsonify({"message":"wrong password"})


        else:
            return make_response(jsonify({"message": "Invalid email, Please try again"}), 409)



# Reset password


@reset_password()
def reset():

    data = request.get_json()
    email = data.get('email')
    
    if email != None:
        
        user = User.query.filter_by(email=email).first()
        
        if user:

            reset_token = create_access_token(identity=user.id)            
            
            if reset_token:

                stored_reset_tokens.add(reset_token)

                response = {
                            'message': 'Use this token to reset your password.',
                            'reset_token': reset_token
                        }
            return jsonify(response), 200
        else:
            
            return jsonify({"message":'User does not exixt, please register'}), 404
    else:
        return jsonify({"message":"Please provide your email"}), 409

"""confirms password reset"""

@confirm_reset_password()
def confirm_reset(reset_token):
    data = request.get_json()
    new_password = data.get('new_password')

    user_id=decode_token(reset_token)["identity"]
    
    if new_password != None:
        try:
            reset_token in stored_reset_tokens
        except InvalidTokenError as error:
            return jsonify({'message':'Reset password token is Invalid, Please request for a new one'}), 401

        try:
            user = User.query.filter_by(id = user_id).first()
            user.password = new_password
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "password reset Successful"})
        except AssertionError as error:
            return jsonify({"error": error.args[0]})

    return jsonify({"meaasage":"Please provide your new password"})

# Logout User

@logout()
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return make_response(jsonify({"message": "Logout Successful"}), 200)

        


# Create new business

@create_business()
@jwt_required
def create_business():

    data = request.get_json()
    business = {'name':data.get('name'), 'category' : data.get('category'), 'location':data.get('location'), 'description':data.get('description')}
    try:
        cleaned_data = business_data(**business)
    except AssertionError as error:
        return jsonify({'error': error.args[0]}), 409

    if cleaned_data:

        
        user = get_jwt_identity()
        # check if the business details already in the list, otherwise create the object in the list
        businesses = Business.query.all()
        available_names = [business.name for business in businesses]
        if cleaned_data['name'] in available_names:
            return make_response(jsonify({"error": "Business already Exist, use another name"}), 409)

        else:
            try:
                business = Business(cleaned_data["name"], cleaned_data["category"], cleaned_data["location"], cleaned_data["description"], userid=user)
                business.save_business()
            except AssertionError as err:
                return jsonify({"error": err.args[0]}), 409

            myresponse = {'name': business.name, 'category': business.category,
                          'location': business.location, 'description': business.description}

        return jsonify({"message":"Available businesses", "business list":myresponse}), 201

# Get all the businesses

@retrieve_all()
def view_businesses():
    businesses = Business.query.all()
    mybusinesses = [{business.id: ["Business Name: "+business.name, "Business Category: "+business.category, "Business Location: "+business.location]
                     for business in businesses}]
    if mybusinesses == [{}]:
        return jsonify({"message": "No Business Entry"}), 404
    else:
        return jsonify({"businesses": mybusinesses}), 200

#Get all the businesses but one businesss per page(pagination implementation)
@retrieve_with_pagination()
def view_businesses_per_page(page_num):
    businesses = Business.query.paginate(per_page=1, page=page_num, error_out=True)
    for business in businesses.items:
        if businesses:
            return jsonify({'name':business.name, 'category':business.category, 
                'location':business.location, 'description':business.description}), 200
        else:
            return  jsonify({"message": "Page not found"}), 404

   

# Get a business by id


@retrieve_business_by_id()
def get_business(id):
    businesses = Business.query.all()
    mybusiness = [business for business in businesses if business.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        return make_response(jsonify({"business": {'name': mybusiness.name,
        'category': mybusiness.category, 'location': mybusiness.location, 
        'description': mybusiness.description}}), 200)
    else:
        return make_response(jsonify({"message": "Business not available", }), 404)

# Update business


@update_business()
@jwt_required
def update_business(id):
    data = request.get_json()
    business = {'name':data.get('name'), 'category' : data.get('category'), 'location':data.get('location'), 'description':data.get('description')}
    try:
        cleaned_data = business_data(**business)
    except AssertionError as error:
        return jsonify({'error': error.args[0]}), 409

    if cleaned_data:

        user = get_jwt_identity()

        businesses = Business.query.all()
        target_business = [business for business in businesses if business.id == id]
        if target_business:
            available_names = [business.name.lower() for business in businesses]

            if cleaned_data["name"].lower() in available_names: 
                return make_response(jsonify({"error": "Business already Exist, use another name"}), 409)

            if user != target_business[0].userid:

                return jsonify({"message": "You cannot update someones Business", }), 404

            try:
                target_business[0].update_business(cleaned_data, issuer_id = user)
            except AssertionError as err:
                return jsonify({"error": err.args[0]}), 409

            return jsonify({"message": "Business Updated", }), 201
        else:
            return jsonify({"message": "Business not available", }), 404

# Delete business


@delete_business()
@jwt_required
def delete_business(id):

    user = get_jwt_identity()
    businesses = Business.query.all()
    target_business = [business for business in businesses if business.id == id]
    
    if target_business:
        target_business = target_business[0]

        if target_business.userid == user:

            target_business.delete()
            return make_response(jsonify({"message": "Business deleted", }), 200)
        
        else:
            return jsonify({"message": 'You cannot delete this business'})
    
    else:
        return make_response(jsonify({"message": "No such Business", }), 404)

#search business
@search_business()
def search_business():

    sql_match = '%'+request.args.get('q')+'%'
    search_results = [{business.id : [business.name, business.location, business.category] 
    for business in Business.query.filter(Business.name.like(sql_match)).all()}]
    
    if search_results == [{}]:
        return jsonify({"message": "No business match found"}), 404
    else:
        return jsonify({"Businesses": search_results}), 200
    
# Add a review for a business


@add_business_review()
@jwt_required
def reviews(businessid):
    data = request.get_json()
    reviewbody = data.get("description")
    # check if the review details already in the list, otherwise create the review object in the list
    mybusiness = [
        business for business in Business.query.all() if business.id == businessid]
    if mybusiness:
        business_review = Review(reviewbody, businessid)
        business_review.save_review()
        return make_response(jsonify({"message": "Review added Successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Business with that ID does not exist"}), 404)


# Get all reviews for a business
@retrieve_all_business_reviews()
def myreviews(businessid):
    business_reviews = Review.query.all()
    target_reviews = [{review.id : [review.businessid, review.reviewbody] 
    for review in business_reviews if review.businessid == businessid}]
    
    if target_reviews == [{}]:
        return make_response(jsonify({"message": "No Reviews available for that Business"}), 404)
    else:
        return make_response(jsonify({"Reviews": target_reviews})), 200
