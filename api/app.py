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
@app.route('/api/v1/auth/user_login',  methods = ['POST'])
def user_login():
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
@app.route('/api/v1/auth/user_logout', methods = ['POST'])
def user_logout():
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
   



if __name__ == '__main__':

    app.run(debug=True)