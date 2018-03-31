import os
import app
import unittest
import tempfile
import json
from flask import jsonify

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data = {"reviewbody":"This is my first best review", "businessid":1}
        self.data2 = {"reviewbody":"This is my second review", "businessid":2}
     

       
        

    def test_reviews(self):
        response = self.app.post('/api/v2/auth/1/reviews', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review added Successfully")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_reviews(self):
        response = self.app.post('/api/v2/auth/2/reviews', data = json.dumps(self.data2) , content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review already Exist, use another description")
        self.assertEqual(response.status_code, 409)

    
    def test_myreviews(self):
        response = self.app.get('/api/v2/auth/1/reviews', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Available reviews")
        self.assertEqual(response.status_code, 200) 
