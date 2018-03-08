from flask import Flask, request, jsonify, make_response
import json 
from models.user import User
from models.business import Business


app = Flask(__name__)

users = []
businesses = []

#Endpoint to Register user and ssaving the details in a list called users
@app.route('/api/v1/auth/register_user',  methods = ['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    #check if the user details already in the list, otherwise add the details in the list
    available_emails = [x.email for x in users]
    if email in available_emails:
        return make_response(jsonify({"status": "NOT_ACCEPTABLE", "message": "User Details Exist"}), 409)
    else:
        user = User(username, email, password)
        users.append(user)
    return make_response(jsonify({"status": "ok", "message": "Registered Successful"}), 201)

#Endpoint to Login user
@app.route('/api/v1/auth/login',  methods = ['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #check if the user details exist in the list, otherwise deny access.
    user = [x for x in users if x.username == username]
    if user:
        if password == user[0].password:
            return make_response(jsonify({"status": "ok", "message": "Login Successful"}), 200)

        else:
            return make_response(jsonify({"status": "Forbidden", "message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({"status": "Forbidden", "message": "Wrong Login Details"}), 409)
   
#Endpoint to Reset password
@app.route('/api/v1/auth/reset_password', methods = ['POST'])
def reset_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    resetpassword = data['resetpassword']
    user = [x for x in users if x.username == username]
    if user and password == user[0].password:
        user[0].reset_password(resetpassword)
        return make_response(jsonify({"status": "ok", "message": "Reset Successful"}), 201)
       
    else:
        return make_response(jsonify({"status": "Forbidden", "message": "Type Different Password"}), 409)
#Logout User
@app.route('/api/v1/auth/logout', methods = ['POST'])
def logout():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #check if the user details exist in the list, otherwise deny access.
    user = [x for x in users if x.username == username]
    if user:
        if password == user[0].password:
            return make_response(jsonify({"status": "ok", "message": "Logout Successful"}), 200)

        else:
            return make_response(jsonify({"status": "Forbidden", "message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({"status": "Forbidden", "message": "Wrong Login Details"}), 409)


#Endpoint to Create new business
@app.route('/api/v1/auth/create_business', methods = ['POST'])
def create_business():
    data = request.get_json()
    name = data["name"]
    category = data["category"]
    location = data["location"]
    description = data["description"]
     #check if the business details already in the list, otherwise create the object in the list
    available_names = [x.name for x in businesses]
    if name in available_names:
        return make_response(jsonify({"status": "Conflict", "message": "Business already Exist, use another name"}), 409)
    else:
        business = Business( name, category, location, description)
        businesses.append(business)
        myresponse = {'name':business.name, 'category':business.category, 'location':business.location, 'description':business.description}
    return make_response(jsonify(myresponse), 201)

#Endpoint to view all the businesses
@app.route('/api/v1/auth/view_businesses', methods = ['GET'])
def view_businesses():
    mybusinesses = [{x.id : [x.name, x.category, x.location] for x in businesses}]
    return make_response(jsonify({"status": "ok", "message": "Available Businesses", "businesses":mybusinesses}), 200)
   

if __name__ == '__main__':

    app.run(debug=True)