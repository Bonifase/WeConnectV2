import os
import app
import unittest
import tempfile
import json
from flask import jsonify
from app import db

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data = {"username":"john", "email":"email@gmail.com","password":"12345"}
        self.data2 = {"username":"Bill", "email":"bill@gmail.com","password":"123456"}
        self.data3 = {"username":"Bills", "email":"bills@gmail.com","password":"1234567"}
        self.data4 = {"username":"james", "email":"jamess@gmail.com", "password":"12345678"}
        self.data5 = {"username":"james", "password":"12345678", "resetpassword":"123456789"}
        self.data6 = {"username":"james", "email":"jamess@gmail.com", "password":"123456789"}

       
        

    def test_register_user(self):
        response = self.app.post('/api/auth/register', data = json.dumps(self.data6) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User Details Exist")
        self.assertEqual(response.status_code, 409)

    def test_duplicate_register(self):
        response2 = self.app.post('/api/auth/register', data = json.dumps(self.data) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "User Details Exist")
        self.assertEqual(response2.status_code, 409)

    def test_login(self):
        response = self.app.post('/api/auth/login', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Login required")
        self.assertEqual(response.status_code, 409)
    def test_unregistered_user(self):
        response = self.app.post('/api/auth/login', data = json.dumps(self.data3) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Login required")
        self.assertEqual(response.status_code, 409)

    def test_reset_password(self):
        response = self.app.post('/api/auth/register', data = json.dumps(self.data4) , content_type = 'application/json')
        self.assertEqual(response.status_code, 409)
        response1 = self.app.post('/api/auth/reset-password', data = json.dumps(self.data5) , content_type = 'application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Token is Missing!")
        self.assertEqual(response1.status_code, 401)
        response2 = self.app.post('/api/auth/login', data = json.dumps(self.data6) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "Login required")
        self.assertEqual(response2.status_code, 409)

    def test_logout(self):
        response = self.app.post('/api/auth/login', data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 409)
        response1 = self.app.post('/api/auth/logout', data = json.dumps(self.data) , content_type = 'application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Token is Missing!")
        self.assertEqual(response1.status_code, 401)
   




if __name__ == '__main__':
    unittest.main()
