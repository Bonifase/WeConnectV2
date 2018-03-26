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
        response = self.app.post('/api/businesses', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)

    def test_duplicate_business(self):
        response1 = self.app.post('/api/businesses', data = json.dumps(self.data2) , content_type = 'application/json')
        self.assertEqual(response1.status_code, 401)
        response2 = self.app.post('/api/businesses', data = json.dumps(self.data2) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "Token is Missing!")
        self.assertEqual(response2.status_code, 401)
    
    def test_view_businesses(self):
        response = self.app.get('/api/api/businesses', data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Token is Missing!")
        self.assertEqual(response.status_code, 401) 

        

if __name__ == '__main__':
    unittest.main()