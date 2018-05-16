from app import app, db
import unittest

import json
from flask import jsonify
from config import app_config

from app.models.models import User

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.app =app.test_client()
        with app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

        # Default user
        self.app.post('/api/v2/auth/register',
                      data=json.dumps(dict(username="username", email="user@gmail.com",password="user123")),
                       content_type='application/json')   
        

    def test_missing_username_key_registration_fails(self):
        """Test API rejects username key that is missing (POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(password = "123we")), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "usernameis missing")
        self.assertEqual(response.status_code, 409)

    def test_invalid_username_registration_fails(self):
        """Test API rejects invalid username registration (POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username= ",", email = "test@gmail.com", password = "test123")),
             content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid username")
        self.assertEqual(response.status_code, 409)

    def test_invalid_email_registrartion_fails(self):
        """Test API rejects invalid password registration(POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username = "username", email = "hfgf", password = "user234")), 
            content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid email")
        self.assertEqual(response.status_code, 409)

    def test_non_string_username_registrartion_fails(self):
        """Test API rejects non-string username registration (POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username = 2, email = "username@gmail.com", password = "user23")),
             content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid username")
        self.assertEqual(response.status_code, 409)

    def test_no_string_email_registrartion_fails(self):
        """Test API rejects non-string email registration (POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username = "username", email = 1, password = "user345")), 
            content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid email")
        self.assertEqual(response.status_code, 409)

    def test_non_string_password_registrartion_fails(self):
        """Test API rejects non-string password registration (POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username = "username", email = "username@gmail.com", password = 1)),
             content_type='application/json')
        result = json.loads(response.data.decode())
        
        self.assertEqual(result["error"], "Invalid password")
        self.assertEqual(response.status_code, 409)

    def test_invalid_password_registration(self):
        """Test API rejects invalid password registration (POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username="user123", password=".", email="user123@gmail.com")),
             content_type='application/json')
        result = json.loads(response.data.decode())
        
        self.assertEqual(result["error"], "Invalid password")
        self.assertEqual(response.status_code, 409)

    def test_new_user_registration_works(self):
        """Test API registers new user successfully (POST request)"""

        response = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username="Bill", email="bill@gmail.com",password="123456")), 
            content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You registered successfully. Please log in")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_user_registration_fails(self):
        """Test API rejects registration of a user email twice (POST request)"""

        response2 = self.app.post(
            '/api/v2/auth/register', data=json.dumps(dict(username="username", email="user@gmail.com",password="user123")), 
            content_type='application/json')

        result2 = json.loads(response2.data.decode())

        self.assertEqual(result2["message"], "User already exists. Please login")
        self.assertEqual(response2.status_code, 409)

    def test_user_login_works(self):
        """Test API logs in users successfully (POST request)"""

        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(dict(username="username", email="user@gmail.com",password="user123")), 
            content_type='application/json')
        result = json.loads(response.data.decode())

        self.assertEqual(result["message"], "You logged in successfully.")
        self.assertEqual(response.status_code, 200)

    def test_wrong_email_login_fails(self):
        """Test API rejects wrong email during login (POST request)"""

        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(dict(email="user3@gmail.com",password="user123")), 
            content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid email, Please try again")
        self.assertEqual(response.status_code, 409)

    def test_empty_login_fails(self):
        """Test API rejects empty user details during login (POST request)"""

        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(dict(email = "", password = "")), content_type='application/json')
        result = json.loads(response.data.decode())

        self.assertTrue(result["message"], "Incomplete entry")
        self.assertEqual(response.status_code, 409)

    def test_unregistered_user_login_fails(self):
        """Test API rejects login requests from unregistered users (POST request)"""

        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(dict(email="someuser@email.com", username="someuser",
                                           password="someuser123")), content_type='application/json')
        result = json.loads(response.data.decode())

        self.assertEqual(result["message"], "Invalid email, Please try again")
        self.assertEqual(response.status_code, 409)

    def test_unavailable_email_not_allowed(self):
        """Test API rejects reset password request from empty email (POST request)"""

        self.app.post('/api/v2/auth/login', data=json.dumps(dict(username="username", email="user@gmail.com",password="user123")),
                      content_type='application/json')
        response1 = self.app.post('/api/v2/auth/reset-password',
                                  data=json.dumps(dict(password="somepassword")), content_type='application/json')
        result1 = json.loads(response1.data.decode())

        self.assertEqual(result1["message"], "Please provide your email")
        self.assertEqual(response1.status_code, 409)

    def test_reset_password_works(self):
        """Test API reset user password (POST request)"""

        response1 = self.app.post('/api/v2/auth/reset-password',
                                  data=json.dumps(dict(email = "user@gmail.com", newpassword = "user234")), 
                                  content_type='application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Use this token to reset your password.")
        self.assertEqual(response1.status_code, 200)
        token = result1["reset_token"]
        response2 = self.app.post(
            '/api/v2/auth/reset-password/{}'.format(token), data=json.dumps(dict(email = "user@gmail.com", 
                new_password = "user234")), content_type='application/json')
        result2 = json.loads(response2.data.decode())

        self.assertEqual(result2["message"], "password reset Successful")
        self.assertEqual(response2.status_code, 200)

    def test_reset_unregistered_user_fails(self):
        """Test API rejects reset password request from unregistered email (POST request)"""

        response1 = self.app.post('/api/v2/auth/reset-password',
                                  data=json.dumps(dict(email = "somemail@gmail.com")), content_type='application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "User does not exixt, please register")


    