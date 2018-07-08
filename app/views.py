from flask import request, jsonify, json

from app.errorhandler import *
import datetime
from jwt.exceptions import InvalidTokenError
from .models import *
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token,  decode_token
)

from app.helpers import clean_data
from app.pagination import get_paginated_list
from app.helpers import *
from app import app

jwt = JWTManager(app)

blacklist = set()
stored_reset_tokens = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/api')
def index():
    return jsonify("Welcome To WeConnect")
# Endpoint to Register user and saving the details in a list called users


@register_user()
def register_user():

    data = request.get_json()
    user = {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': data.get('password')}
    try:
        cleaned_data = clean_data(**user)
    except AssertionError as error:
        return jsonify({'message': error.args[0]}), 409

    if cleaned_data:
        users = User.query.all()
        available_emails = [user.email for user in users]

        if data.get('email') in available_emails:
            return jsonify({
                "message": "User already exists. Please login"}), 409
        else:
            try:
                user = User(
                    cleaned_data['username'],
                    cleaned_data['email'], cleaned_data['password'])
                user.register_user()
            except AssertionError as err:
                return jsonify({'message': err.args[0]}), 409

        return jsonify({
            "message": "You registered successfully. Please log in"}), 201
# Login user


@login()
def login():

    data = request.get_json()
    print(data)
    user = {'email': data.get('email'), 'password': data.get('password')}

    try:
        cleaned_data = clean_data(**user)
    except AssertionError as error:
        return jsonify({'message': error.args[0]}), 401

    user = User.query.filter_by(email=cleaned_data["email"]).first()

    if user:

        if Bcrypt().check_password_hash(user.password, cleaned_data[
                "password"]):
            access_token = create_access_token(
                identity=user.id, expires_delta=datetime.timedelta(minutes=60))
            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token,
                    'username': user.username,
                    'userId': user.id
                }
            return jsonify(response), 200
        else:
            return jsonify({"message": "wrong password"}), 401
    return jsonify({
        "message": "Invalid email, Please try again"}), 401
# Reset password


@reset_password()
def reset():

    data = request.get_json()
    email = data.get('email')
    if email is not None:
        user = User.query.filter_by(email=email).first()
        if user:

            reset_token = create_access_token(identity=user.id)
            if reset_token:

                stored_reset_tokens.add(reset_token)

                response = {
                    'message': 'reset your password token.',
                    'reset_link': '/api/v2/auth/reset-password/{}'.format(reset_token)
                }
            return jsonify(response), 200
        else:
            return jsonify(
                {"message": 'User does not exixt, please register'}), 404
    else:
        return jsonify({"message": "Please provide your email"}), 409


"""confirms password reset"""


@confirm_reset_password()
def confirm_reset(reset_token):
    data = request.get_json()
    new_password = data.get('new_password')

    user_id = decode_token(reset_token)["identity"]
    if new_password is not None:
        try:
            reset_token in stored_reset_tokens
        except InvalidTokenError as error:
            return jsonify(
                {
                    'message': 'Invalid Reset password token'}), 401

        try:
            user = User.query.filter_by(id=user_id).first()
            user.password = new_password
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "password reset Successful"})
        except AssertionError as error:
            return jsonify({"message": error.args[0]})

    return jsonify({"message": "Please provide your new password"})

# Logout User


@logout()
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"message": "Logout Successful", }), 200

# Create new business


@create_business()
@jwt_required
def create_business():

    data = request.get_json()
    business = {
        'name': data.get('name'),
        'category': data.get('category'),
        'location': data.get('location'),
        'description': data.get('description')}
    try:
        cleaned_data = business_data(**business)
    except AssertionError as error:
        return jsonify({'message': error.args[0]}), 409

    if cleaned_data:
        user = get_jwt_identity()
        # check if the business details already in the list.
        # create the object in the list
        available_names = [
            business.name.lower() for business in Business.businesses()]
        if cleaned_data['name'].lower() in available_names:
            return jsonify(
                {"message": "Business already Exist, use another name"}), 409
        else:
            try:
                business = Business(
                    cleaned_data["name"], cleaned_data["category"],
                    cleaned_data["location"],
                    cleaned_data["description"], userid=user)
                business.save_business()
            except AssertionError as err:
                return jsonify({"message": err.args[0]}), 409

            myresponse = {
                'Business Name': business.name,
                'Business Category': business.category,
                'location': business.location,
                'Business Description': business.description,
                "Date Created": "{:%m/%d/%Y}".format(business.date_created)}

    return jsonify(
        {
            "message": "You created this business",
            "business list": myresponse}), 201


"""Get all the businesses"""


@retrieve_all()
def view_businesses():
    mybusinesses = [
        {"_id": business.id,
         "owner": business.userid,
            "Business_Name": business.name,
            "Business_category": business.category,
            "Business_location": business.location,
            'Business_description': business.description,
            "Date_Created": "{:%m/%d/%Y}".format(
                business.date_created)} for business in Business.businesses()]

    if mybusinesses == []:
        return jsonify({"message": "No Business Entry"}), 404
    else:
        return jsonify({"businesses": mybusinesses}), 200
# Get a business by id


@retrieve_business_by_id()
def get_business(id):
    mybusiness = [business for business in Business.businesses(
    ) if business.id == id]
    if mybusiness:
        target_business = mybusiness[0]
        print("hahahahahaha", target_business)
        return jsonify({"business": {
            '_id': target_business.id,
            "owner": target_business.userid,
            'Name': target_business.name,
            'Category': target_business.category,
            'Location': target_business.location,
            'Description': target_business.description,
            "Created": "{:%m/%d/%Y}".format(
                target_business.date_created)}}), 200
    else:
        return jsonify({"message": "Business not available", }), 404
# Update business


@update_business()
@jwt_required
def update_business(businessid):
    data = request.get_json()
    business = {
        'name': data.get('name'),
        'category': data.get('category'),
        'location': data.get('location'),
        'description': data.get('description')}
    try:
        cleaned_data = business_data(**business)
    except AssertionError as error:
        return jsonify({'message': error.args[0]}), 409

    if cleaned_data:

        user = get_jwt_identity()

        target_business = Business.query.filter_by(id=businessid).first()
        if target_business:
            available_names = [business.name.lower(
            ) for business in Business.businesses()]
            if user != target_business.userid:

                return jsonify(
                    {"message": "You cannot update someones Business", }), 404

            try:
                target_business.update_business(cleaned_data, issuer_id=user)
            except AssertionError as err:
                return jsonify({"message": err.args[0]}), 409

            return jsonify({"message": "Business Updated", }), 201
        else:
            return jsonify({"message": "Business not available", }), 404
# Delete business


@delete_business()
@jwt_required
def delete_business(id):

    user = get_jwt_identity()
    target_business = [
        business for business in Business.businesses(
        ) if business.id == id]
    if target_business:
        target_business = target_business[0]

        if target_business.userid == user:

            target_business.delete()
            return jsonify({"message": "Business deleted", }), 200
        else:
            return jsonify({"message": 'You cannot delete this business'})
    else:
        return jsonify({"message": "No such Business", }), 404

# search,filter business and implements pagination


@search_business()
def search_business():
    """business URL template"""
    business_href = "/businesses/search?page=%s"
    businesses = [{"_id": business.id,
                   "owner": business.userid,
                   "Business_Name": business.name,
                   "Business_category": business.category,
                   "Business_location": business.location,
                   'Business_description': business.description,
                   "Date_Created": "{:%m/%d/%Y}".format(
                       business.date_created)}
                  for business in Business.query.all()]
    if businesses == [{}]:
        return jsonify({"message": "No businesses"})
    """search a business"""
    if "q" in request.args:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        sql_match = '%'+request.args.get('q')+'%'
        businesses = [{"_id": business.id,
                       "owner": business.userid,
                       "Business_Name": business.name,
                       "Business_category": business.category,
                       "Business_location": business.location,
                       'Business_description': business.description,
                       "Date_Created": "{:%m/%d/%Y}".format(
                           business.date_created)} for business in Business.query.filter(
            Business.name.ilike(sql_match)).all()]
        response = {"results": "ok",
                    "business_href": business_href % page,
                    "filteredBusinesses": businesses}

        return jsonify(response)
    """Filter business by category"""
    if "category" in request.args:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        businesses = [{"_id": business.id,
                       "owner": business.userid,
                       "Business_Name": business.name,
                       "Business_category": business.category,
                       "Business_location": business.location,
                       'Business_description': business.description,
                       "Date_Created": "{:%m/%d/%Y}".format(
                           business.date_created)} for business in Business.query.filter_by(
            category=request.args.get('category')).all()]
        business_href += "&category: " + request.args.get('category')
        response = {"results": "ok",
                    "business_href": business_href % page,
                    "filteredBusinesses": businesses}

        return jsonify(response)
    """Filter business by location"""

    if "location" in request.args:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        businesses = [{"_id": business.id,
                       "owner": business.userid,
                       "Business_Name": business.name,
                       "Business_category": business.category,
                       "Business_location": business.location,
                       'Business_description': business.description,
                       "Date_Created": "{:%m/%d/%Y}".format(
                           business.date_created)} for business in Business.query.filter_by(
            location=request.args.get('location')).all()]
        business_href += "&location: " + request.args.get('location')
        response = {"results": "ok",
                    "business_href": business_href % page,
                    "filteredBusinesses": businesses}

        return jsonify(response)

    if "page" in request.args:
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid pagination limit value"})

        pagination = get_paginated_list(
            page=page, limit=limit, url="/businesses/search")
        paginated_data = pagination['results']
        previous_page = pagination['previous']
        next_page = pagination["next"]
        count = pagination['count']
        limit = pagination['limit']
        page = pagination['page']
        mybusinesses = [{
            "Next_page": next_page,
            "Prevoius_page": previous_page,
            "_id": business.id,
            "owner": business.userid,
            "Business_Name": business.name,
            "Business_category": business.category,
            "Business_location": business.location,
            'Business_description': business.description,
            "Date_Created": "{:%m/%d/%Y}".format(
                business.date_created)}
            for business in paginated_data]
        response = {
            "businesses": mybusinesses, "pagination": {"per_page": limit,
                                                       "page": page,
                                                       "total_pages": count, "Prevoius_page": previous_page,
                                                       "Next_page": next_page}}

        return jsonify(response)


@add_business_review()
@jwt_required
def reviews(businessid):
    data = request.get_json()
    reviewbody = data.get("description")
    review = {'description': data.get('description')}
    try:
        cleaned_data = review_data(**review)
    except AssertionError as error:
        return jsonify({'message': error.args[0]}), 409

    if cleaned_data:
        user_id = get_jwt_identity()

        # check if the review details already in the list
        target_business = Business.query.filter_by(id=businessid).first()
        if target_business:

            business_review = Review(reviewbody, businessid, user_id)
            business_review.save_review()
            return jsonify({"message": "Review added Successfully"}), 201
        else:
            return jsonify({
                "message": "Business with that ID does not exist"}), 404

# Get all reviews for a business


@retrieve_all_business_reviews()
def myreviews(businessid):
    business_reviews = Review.query.all()
    target_reviews = [
        {"_id": review.id,
            "Business_Id": review.businessid,
            "body": review.reviewbody} for review in business_reviews if review.businessid == businessid]
    if target_reviews == [{}]:
        return jsonify({
            "message": "No Reviews available for that Business"}), 404
    else:
        return jsonify({"Reviews": target_reviews}), 200
