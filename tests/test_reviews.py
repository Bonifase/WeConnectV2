import os
from app import app
import unittest
import tempfile
import json
from flask import jsonify

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"reviewbody":"This is my first review", "businessid":1}
        self.data2 = {"reviewbody":"This is my second review", "businessid":2}
        self.data3 = {"username":"john", "email":"email@gmail.com","password":"&._12345"}
        

       
        

    def test_reviews(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data3) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data3) , content_type = 'application/json')
        response = self.app.post('/api/v1/auth/1/reviews', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review added Successfully")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_reviews(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data3) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data3) , content_type = 'application/json')
        response1 = self.app.post('/api/v1/auth/2/reviews', data = json.dumps(self.data2) , content_type = 'application/json')
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Review added Successfully")
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post('/api/v1/auth/2/reviews', data = json.dumps(self.data2) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "Review already Exist, use another description")
        self.assertEqual(response2.status_code, 409)
    
    def test_myreviews(self):
        self.app.post('/api/v1/auth/register', data = json.dumps(self.data3) , content_type = 'application/json')
        self.app.post('/api/v1/auth/login', data = json.dumps(self.data3) , content_type = 'application/json')
        response = self.app.get('/api/v1/auth/1/reviews', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data2["reviewbody"], result['Reviews'][0]['1'][1])
        self.assertEqual(response.status_code, 200) 
