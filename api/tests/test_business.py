# import os
import app
import unittest
import tempfile
import json
from flask import jsonify

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data = { "name":"easyE", "category":"hardware", "location":"Mombasa", "description":"Selling hardware products" }
        self.data2 = { "name":"Dlinks", "category":"software", "location":"Nairobi", "description":"Selling software products"}
        self.data3 = { "name":"Ecosoft", "category":"software", "location":"Nakuru", "description":"Selling software products"}
        

    def test_create_business(self):
        response = self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data['name'], result['name'])
        self.assertEqual(response.status_code, 201)

    def test_duplicate_business(self):
        response1 = self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data2) , content_type = 'application/json')
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post('/api/v1/auth/businesses', data = json.dumps(self.data2) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "Business already Exist, use another name")
        self.assertEqual(response2.status_code, 409)
    
    def test_view_businesses(self):
        response = self.app.get('/api/v1/auth/businesses', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Available Businesses")
        self.assertEqual(response.status_code, 200) 

        

if __name__ == '__main__':
    unittest.main()