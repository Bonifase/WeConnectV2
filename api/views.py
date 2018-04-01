from app import app
from models.models import *
from flask import request,make_response, jsonify
from flask_login import LoginManager, login_required, logout_user
import json, jwt, datetime	
import flask_whooshalchemy as wa
from functools import wraps


login_manager = LoginManager()
login_manager.init_app(app)


wa.whoosh_index(app,Business)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is Missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id = data['id']).first()
        except:
            return jsonify({'message':'Token is Invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


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
    #auth = request.authorization
    data = request.get_json()
    #check if the user details exist in the list, otherwise deny access.
    # if not auth or not auth.username or not auth.password:
    #     return make_response(jsonify({"status": "Conflict", "message": "Login required"}), 409)

    user = User.query.filter_by(username=data['username']).first()
    if user:
        if user.password == data['password']:
            user_token = jwt.encode({'id':user.id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'])
            return make_response(jsonify({"status": "ok", "user_token": user_token.decode()}), 200)

        else:
            return make_response(jsonify({"status": "Conflict", "message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({"status": "Conflict", "message": "Wrong Login Details"}), 409)
   
#Reset password
@app.route('/api/v2/auth/reset-password', methods = ['POST'])
@token_required
def reset_password(current_user):
    data = request.get_json()
    resetpassword = data['resetpassword']
    user = current_user
    if resetpassword != user.password:
        user.password = resetpassword
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"status": "Created", "message": "Reset Successful"}), 201)
       
    else:
        return make_response(jsonify({"status": "Conflict", "message": "Type Different Password"}), 409)
#Logout User
@app.route('/api/v2/auth/logout', methods = ['POST'])
@token_required
def logout(current_user):
    user = current_user
    if user:
        user.authenticated = False
        db.session.commit()
        logout_user()
        return make_response(jsonify({"status": "ok", "message": "Logout Successful"}), 200)

    else:
        return make_response(jsonify({"status": "Conflict", "message": "Wrong Login Details"}), 409)


#Create new business
@app.route('/api/v2/auth/businesses', methods = ['POST'])
@token_required
def create_business(current_user):
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
        db.session.add(business)
        db.session.commit()
        myresponse = {'name':business.name, 'category':business.category, 'location':business.location, 'description':business.description, 'Date Created':business.date_created}
    return make_response(jsonify(myresponse), 201)

#Get all the businesses
@app.route('/api/v2/auth/businesses', methods = ['GET'])
@token_required
def view_businesses(current_user):
    businesses = Business.query.all()
    mybusinesses = [{x.id : [x.name, x.category, x.location, x.description, 'Created on:'+ str(x.date_created) ] for x in businesses}]
    return make_response(jsonify({"status": "ok", "message": "All Businesses", "Available Businesses":mybusinesses}), 200)

#Get all the businesses but one businesss per page(pagination implementation)
@app.route('/api/api/businesses/<int:page_num>', methods = ['GET'])
@token_required
def view_businesses_per_page(current_user, page_num):
    mybusinesses = Business.query.paginate(per_page=1, page=page_num, error_out=True)
    for business in mybusinesses.items:
        return make_response(jsonify({'name':business.name, 'category':business.category, 'location':business.location, 'description':business.description}), 200)

#Get a business by id
@app.route('/api/v2/auth/business/<int:id>/')
@token_required
def get_business(current_user, id):
    businesses = Business.query.all()
    mybusiness = [x for x in businesses if x.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        return  make_response(jsonify({"status": "ok", "message": "Available Business", "business":{'name':mybusiness.name, 'category':mybusiness.category, 'location':mybusiness.location, 'description':mybusiness.description}}), 200)
    else:
         return  make_response(jsonify({"status": "not found", "message": "No such Businesses",}), 404)

#search business
@app.route('/api/search', methods = ['GET'])
@token_required
def search_business(current_user):
    results = Business.query.whoosh_search(request.args.get('query')).all()

    return jsonify(results)

#Update business
@app.route('/api/v2/auth/business/<int:id>/', methods = ['PUT'])
@token_required
def update_business(current_user, id):
    data = request.get_json()
    newname = data["name"]
    newcategory = data["category"]
    newlocation = data["location"]
    newdescription = data["description"]
    businesses = Business.query.all()
    mybusiness = [x for x in businesses if x.id == id]
    if mybusiness:
        mybusiness[0].name = newname
        mybusiness[0].category = newcategory
        mybusiness[0].location = newlocation
        mybusiness[0].description = newdescription
        db.session.commit()
        return  make_response(jsonify({"status": "Created", "message": "Business Updated",}), 201)
    else:
         return  make_response(jsonify({"status": "not found", "message": "No such Businesses",}), 404)


#Delete business
@app.route('/api/v2/auth/business/<int:id>/', methods = ['DELETE'])
@token_required
def delete_business(current_user, id):
    #mybusiness = [x for x in businesses if x.id == id]
    business = Business.query.filter_by(id=id).first()
    if business:
        #mybusiness = mybusiness[0]
        db.session.delete(business)
        db.session.commit()
        return  make_response(jsonify({"status": "Deleted", "message": "Business deleted",}), 201)
    else:
         return  make_response(jsonify({"status": "not found", "message": "No such Businesses",}), 404)


#Add a review for a business
@app.route('/api/v2/auth/<int:businessid>/reviews', methods = ['POST'])
@token_required
def reviews(current_user, businessid):
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
@token_required
def myreviews(current_user, businessid):
    business_reviews = Review.query.all()
    myreviews = [{x.id : [x.businessid, x.reviewbody] for x in business_reviews}]
    return make_response(jsonify({"status": "ok", "message": "Available reviews", "Reviews":myreviews}), 200)
