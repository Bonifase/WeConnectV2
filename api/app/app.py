from flask import Flask, request, jsonify, make_response, session
import json 

from models.user import User
from models.business import Business
from models.review import Review


app = Flask(__name__)

business_reviews = []

#Endpoint to Register user and ssaving the details in a list called users
@app.route('/api/v1/auth/register',  methods = ['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    #check if the user details already in the list, otherwise add the details in the list
    available_emails = [x.email for x in User.users]
    if email in available_emails:
        return make_response(jsonify({"message": "User Details Exist"}), 409)
    else:
        try:
            user = User.register_user(username, email, password)
        except AssertionError as err:
            return jsonify({'error': err.args[0]})

    return make_response(jsonify({ "message": user.username}), 201)

#Login user
@app.route('/api/v1/auth/login',  methods = ['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #check if the user details exist in the list, otherwise deny access.
    if data['username'] == "" or data['password'] == "":
        return make_response(jsonify({"message": "Incomplete entry"}), 401)
    user = [x for x in User.users if x.username == username]
    if user:
        if password == user[0].password:
            session['username'] = username
            return make_response(jsonify({"message": "Login Successful"}), 200)

        else:
            return make_response(jsonify({"message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({"message": "Wrong Login Details"}), 409)
   
#Reset password
@app.route('/api/v1/auth/reset-password', methods = ['POST'])
def reset_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    newpassword = data['newpassword']
    user = [x for x in User.users if x.username == username]
    if user and password != user[0].password:
        return make_response(jsonify({"message": "Enter your Current Password"}), 409)
    elif newpassword == user[0].password:
        return make_response(jsonify({"message": "Use a Different New Password"}), 409)
       
    else:
        user[0].reset_password(newpassword)
        return make_response(jsonify({"message": "Reset Successful"}), 201)
        
#Logout User
@app.route('/api/v1/auth/logout', methods = ['POST'])
def logout():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #check if the user details exist in the list, otherwise deny access.
    user = [x for x in User.users if x.username == username]
    if user:
        if password == user[0].password:
            return make_response(jsonify({"message": "Logout Successful"}), 200)

        else:
            return make_response(jsonify({ "message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({ "message": "Wrong Login Details"}), 409)


#Create new business
@app.route('/api/v1/auth/businesses', methods = ['POST'])
def create_business():
    data = request.get_json()
    name = data["name"]
    category = data["category"]
    location = data["location"]
    description = data["description"]
     #check if the business details already in the list, otherwise create the object in the list
    available_names = [x.name for x in Business.businesses]
    if name in available_names:
        return make_response(jsonify({"error": "Business already Exist, use another name"}), 409)

    else:
        try:
            business = Business.register_business(name, category, location, description)
        except AssertionError as err:
            return jsonify({'error': err.args[0]})
        myresponse = {'name':business.name, 'category':business.category, 'location':business.location, 'description':business.description}
    return make_response(jsonify(myresponse), 201)

#Get all the businesses
@app.route('/api/v1/auth/businesses', methods = ['GET'])
def view_businesses():
    mybusinesses = [{x.id : [x.name, x.category, x.location] for x in Business.businesses}]
    if mybusinesses == [{}]:
        return make_response(jsonify({"businesses":"No Business Entry"}), 404)
    else:
        return make_response(jsonify({"businesses":mybusinesses}), 200)

#Get a business by id
@app.route('/api/v1/auth/business/<int:id>/')
def get_business(id):
    mybusiness = [x for x in Business.businesses if x.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        return  make_response(jsonify({"business":{'name':mybusiness.name,
         'category':mybusiness.category, 'location':mybusiness.location, 'description':mybusiness.description}}), 200)
    else:
         return  make_response(jsonify({"message": "Business not available",}), 404)

#Update business
@app.route('/api/v1/auth/business/<int:id>', methods = ['PUT'])
def update_business(id):
    data = request.get_json()
    newname = data["name"]
    newcategory = data["category"]
    newlocation = data["location"]
    newdescription = data["description"]
    mybusiness = [x for x in Business.businesses if x.id == id]
    if mybusiness:
        mybusiness[0].update_business(newname, newcategory, newlocation, newdescription)
        return  make_response(jsonify({ "message": "Business Updated",}), 201)
    else:
         return  make_response(jsonify({"message": "Businesses not available",}), 404)

#Delete business
@app.route('/api/v1/auth/business/<int:id>/', methods = ['DELETE'])
def delete_business(id):
    mybusiness = [x for x in Business.businesses if x.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        Business.businesses.remove(mybusiness)
        return  make_response(jsonify({ "message": "Business deleted",}), 200)
    else:
         return  make_response(jsonify({"message": "No such Businesses",}), 404)

#Add a review for a business
@app.route('/api/v1/auth/<int:businessid>/reviews', methods = ['POST'])
def reviews(businessid):
    data = request.get_json()
    reviewbody = data["reviewbody"]
    businessid = data['businessid']
     #check if the review details already in the list, otherwise create the review object in the list
    available_reviewbodies = [x.reviewbody for x in business_reviews ]
    if reviewbody in available_reviewbodies:
        return make_response(jsonify({ "message": "Review already Exist, use another description"}), 409)
    else:
        business_review = Review(reviewbody, businessid)
        business_reviews.append(business_review)
    return make_response(jsonify({"message": "Review added Successfully"}), 201)

#Get all reviews for a business
@app.route('/api/v1/auth/<int:businessid>/reviews', methods = ['GET'])
def myreviews(businessid):
    myreviews = [{x.id : [x.businessid, x.reviewbody] for x in business_reviews}]
    if myreviews == [{}]:
        return make_response(jsonify({"message": "No Reviews available"}), 404)
    else:
        return make_response(jsonify({"Reviews":myreviews}), 200)




if __name__ == '__main__':

    app.run(debug=True)