import os
from app import app, db
import unittest
import tempfile
import json
from flask import jsonify
from config import app_config

from app.models.models import Review


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.app = app.test_client()
        self.data = {"description": "This is my first review"}
        self.data3 = {"username": "john",
                      "email": "email@gmail.com", "password": "&._12345"}
        self.data4 = {"name": "easyE", "category": "hardware",
                      "location": "Mombasa", "description": "Selling hardware products"}

        with app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all() 
            #default user
            self.app.post('/api/v2/auth/register', data = json.dumps(self.data3) , content_type = 'application/json')
            self.login_user = self.app.post('/api/v2/auth/login', data = json.dumps(self.data3), content_type = 'application/json')
            result = json.loads(self.login_user.data.decode())
            self.user_token = result['access_token'] 
            self.app.post('/api/v2/businesses', headers= {'x-access-token':self.user_token}, data = json.dumps(self.data4), content_type = 'application/json')

    


    def test_add_reviews_works(self):
        
        response = self.app.post(
            'api/v2/1/reviews', data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review added Successfully")
        self.assertEqual(response.status_code, 201)

    # def test_invalid_entry_entry_fails(self):
        
    #     response = self.app.post(
    #         '/a/1/reviews', data=json.dumps(self.data1), headers= {'x-access-token':self.user_token}, content_type='application/json')
    #     result = json.loads(response.data.decode())
    #     self.assertEqual(result["error"], "Check your entry")
    #     self.assertEqual(response.status_code, 409)

    # def test_empty_reviews_fails(self):
        
    #     response = self.app.post(
    #         '/a/1/reviews', data=json.dumps(self.data2), headers= {'x-access-token':self.user_token}, content_type='application/json')
    #     result = json.loads(response.data.decode())
    #     self.assertEqual(result["error"], "Empty review not allowed")
    #     self.assertEqual(response.status_code, 409)

    # def test_short_reviews_fails(self):
        
    #     response = self.app.post(
    #         '/api/v2/1/reviews', data=json.dumps(dict(description="l")), headers= {'x-access-token':self.user_token}, content_type='application/json')
    #     result = json.loads(response.data.decode())
    #     print(result)
    #     self.assertEqual(result["error"], "Review too short")
    #     self.assertEqual(response.status_code, 409)

    def test_add_reviews_for_unavailable_business_fails(self):
        
        response = self.app.post(
            '/api/v2/5/reviews', data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "Business with that ID does not exist")
        self.assertEqual(response.status_code, 404)

    def test_available_reviews_works(self):
        
        self.app.post('/api/v2/1/reviews',
                      data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        response = self.app.get(
            '/api/v2/1/reviews', data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        print(result)
        self.assertIn(self.data["description"], result["Reviews"][0]["1"][1])
        self.assertEqual(response.status_code, 200)

    def test_unvailable_reviews_fails(self):
        
        self.app.post('/api/v2/1/reviews', 
                     data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        response = self.app.get('/api/v2/5/reviews', headers= {'x-access-token':self.user_token},
                                content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "No Reviews available for that Business")
        self.assertEqual(response.status_code, 404)