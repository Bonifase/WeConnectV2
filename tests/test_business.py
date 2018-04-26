mport app
import unittest
import json
from app import app, db
from models.models import * 
from flask import jsonify



class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = { "name":"easyE", "category":"hardware", "location":"Mombasa", "description":"Selling hardware products" }
        self.data2 = { "name":"Dlink", "category":"software", "location":"Nairobi", "description":"Selling software products"}
        self.data3 = { "name":"Ecosoft", "category":"software", "location":"Nakuru", "description":"Selling software products"}
        self.data4 = {"username":"test", "email":"test@gmail.com","password":"test123"}
        with app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()
            

    def test_create_business(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data4) , content_type = 'application/json')
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response = self.app.post('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data['name'], result['name'])
        self.assertEqual(response.status_code, 201)
        

    def test_duplicate_business(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data4) , content_type = 'application/json')
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response1 = self.app.post('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data2) , content_type = 'application/json')
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data2) , content_type = 'application/json')
        result2 = json.loads(response2.data.decode())
        self.assertEqual(result2["message"], "Business already Exist, use another name")
        self.assertEqual(response2.status_code, 409)
        
    
    def test_view_businesses(self):
        response = self.app.post('/api/v2/auth/register', data = json.dumps(self.data4) , content_type = 'application/json')
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
        result = json.loads(response.data.decode())
        user_token = result['user_token']
        response = self.app.get('/api/v2/auth/businesses', headers= {'x-access-token':user_token}, data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "All Businesses")
        self.assertEqual(response.status_code, 200) 

        

if __name__ == '__main__':
    unittest.main()