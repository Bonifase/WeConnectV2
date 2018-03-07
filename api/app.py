from flask import Flask, request, jsonify, make_response
import json 
from models.user import User


app = Flask(__name__)

users = []

#Register user and ssaving the details in a list called users
@app.route('/v1/register_user',  methods = ['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    #check if the user details already in the list, otherwise add the details in the list
    available_emails = [x.email for x in users]
    if email in available_emails:
        return make_response(jsonify({"status": "NOT_ACCEPTABLE", "message": "User Details Exist"}), 406)
    else:
        user = User(username, email, password)
        users.append(user)
    return make_response(jsonify({"status": "ok", "message": "Registered Successful"}), 201)

#Login user
@app.route('/v1/user_login',  methods = ['POST'])
def user_login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #check if the user details exist in the list, otherwise deny access.
    available_usernames = [x.username for x in users]
    available_passwords = [x.password for x in users]
    if username in available_usernames and password in available_passwords:
        return make_response(jsonify({"status": "ok", "message": "Login Successful"}), 200)
    else:
        return make_response(jsonify({"status": "Forbidden", "message": "Wrong Login Details"}), 406)
   

if __name__ == '__main__':

    app.run(debug=True)