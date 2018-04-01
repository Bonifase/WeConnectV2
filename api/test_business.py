# import os
import app
import unittest
import tempfile
import json
from app import app, db
from models.models import *
from flask import jsonify

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data = { "name":"easyE", "category":"hardware", "location":"Mombasa", "description":"Selling hardware products" }
        self.data2 = { "name":"Dlink", "category":"software", "location":"Nairobi", "description":"Selling software products"}
        self.data3 = { "name":"Ecosoft", "category":"software", "location":"Nakuru", "description":"Selling software products"}
        self.data4 = {"username":"Bill", "email":"bill@gmail.com","password":"123456"}
        db.create_all()
        

    def test_create_business(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response = self.app.post('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Business already Exist, use another name")
        self.assertEqual(response.status_code, 409)

    def test_duplicate_business(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response1 = self.app.post('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data2) , content_type = 'application/json')
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data2) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertIn(self.data2['name'], result2['name'])
        self.assertEqual(response2.status_code, 201)
    
    def test_view_businesses(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response = self.app.get('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "All Businesses")
        self.assertEqual(response.status_code, 200) 

        

if __name__ == '__main__':
    unittest.main()