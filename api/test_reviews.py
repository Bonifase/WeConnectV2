import os
import app
import unittest
import tempfile
import json
from app import app, db
from models.models import *
from flask import jsonify

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"reviewbody":"This is my first best review", "businessid":1}
        self.data2 = {"reviewbody":"This is my second review", "businessid":2}
        self.data3 = {"username":"Bill", "email":"bill@gmail.com","password":"123456"}
        db.create_all()
     

       
        

    def test_reviews(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data3), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response = self.app.post('/api/v2/auth/1/reviews', headers= {'x-access-token':user_token}, data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review added Successfully")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_reviews(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data3), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response = self.app.post('/api/v2/auth/2/reviews', headers= {'x-access-token':user_token}, data = json.dumps(self.data2) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review already Exist, use another description")
        self.assertEqual(response.status_code, 409)

    
    def test_myreviews(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data3), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response = self.app.get('/api/v2/auth/1/reviews', headers= {'x-access-token':user_token}, data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Available reviews")
        self.assertEqual(response.status_code, 200) 
