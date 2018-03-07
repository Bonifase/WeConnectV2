from flask import request, jsonify, make_response
from flask_api import FlaskAPI, status, exceptions, response
from models.user import User


app = FlaskAPI(__name__)
users = []

@app.route('/v1/register_user',  methods = ['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    user = User(username, email, password)
    users.append(user)

    return '', status.HTTP_201_CREATED


@app.route('/v1/user_login', methods = ['POST'])
def user_login():
    data = request.get_json(force = True)
    username = data['username']
    password = data['password']
    if username in users and password in users:
        response.status_code = 202

    return response

if __name__ == '__main__':

    app.run(debug=True)