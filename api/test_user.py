import os
import app
import unittest
from app import app, db
from models.models import User
import tempfile
import json
from flask import jsonify

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app =app.test_client()
        self.data = {"username":"johnny", "email":"emais@gmail.com","password":"boni"}
        self.data2 = {"username":"Bill", "email":"bill@gmail.com","password":"123456"}
        self.data3 = {"username":"Bills", "email":"bills@gmail.com","password":"1234567"}
        self.data4 = {"username":"james", "email":"jamess@gmail.com", "password":"james123"}
        self.data5 = {"username":"james", "password":"123456789", "resetpassword":"james1234"}
        self.data6 = {"username":"james", "email":"jamess@gmail.com", "password":"james1234"}
        with app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

       
        

    def test_register_user(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Registered Successful")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_register(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Registered Successful")
        self.assertEqual(response.status_code, 201)
        response2 = self.app.post('/api/v2/auth/register', data = json.dumps(self.data) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "User Details Exist")
        self.assertEqual(response2.status_code, 409)

    def test_login(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data2) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data2), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['user_token'])
        self.assertEqual(response.status_code, 200)
    def test_unregistered_user(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data3) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Wrong Login Details")
        self.assertEqual(response.status_code, 409)

    def test_reset_password(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data4) , content_type = 'application/json')
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response1 = self.app.post('/api/v2/auth/reset-password', headers= {'x-access-token':user_token}, data = json.dumps(self.data5) , content_type = 'application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Reset Successful")
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post('/api/v2/auth/login', data = json.dumps(self.data6) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertTrue(result2['user_token'])
        self.assertEqual(response2.status_code, 200)

    def test_logout(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data2) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data2), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response1 = self.app.post('/api/v2/auth/logout', headers= {'x-access-token':user_token}, data = json.dumps(self.data2) , content_type = 'application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Logout Successful")
        self.assertEqual(response1.status_code, 200)
   




if __name__ == '__main__':
    unittest.main()
