# import os
from app import app
import unittest
import tempfile
import json
from flask import jsonify

from app.models.business import Business

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = { "name":"easyE", "category":"hardware", "location":"Mombasa", "description":"Selling hardware products" }
        self.data5 = { "name":"Ecosoft", "category":"software", "location":"Nakuru", "description":"Selling software products"}
        self.data6 = {"username":"john", "email":"email@gmail.com","password":"&._12345"}

       
    def tearDown(self):
        Business.class_counter = 1
        del Business.businesses[:]
        

    def test_unlogged_in_users(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data6) , content_type = 'application/json')
        response = self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["Unauthorised"], "Please login first")
        self.assertEqual(response.status_code, 401)

    def test_create_business(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data6) , content_type = 'application/json')
        response = self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data['name'], result['name'])
        self.assertEqual(response.status_code, 201)

    def test_duplicate_business(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        response = self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Business already Exist, use another name")
        self.assertEqual(response.status_code, 409)
    
    def test_view_businesses(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        response = self.app.get('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data['name'], result['businesses'][0]['1'][0])
        self.assertEqual(response.status_code, 200) 

    def test_update_business(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        response = self.app.put('/api/v1/auth/business/1',  data = json.dumps(self.data5), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business Updated")
        self.assertEqual(response.status_code, 201)
    
    def test_delete_business(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data6) , content_type = 'application/json')
        self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        response = self.app.delete('/api/v1/auth/business/1/',  data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business deleted")
        self.assertEqual(response.status_code, 200)

        

if __name__ == '__main__':
    unittest.main()