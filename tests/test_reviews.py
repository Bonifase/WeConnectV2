import os
from app import app
import unittest
import tempfile
import json
from flask import jsonify

from app.models.review import Review


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"description": "This is my first review"}
        self.data3 = {"username": "john",
                      "email": "email@gmail.com", "password": "&._12345"}
        self.data4 = {"name": "easyE", "category": "hardware",
                      "location": "Mombasa", "description": "Selling hardware products"}

    def tearDown(self):
        del Review.business_reviews[:]

    def test_logged_in_users(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data3), content_type='application/json')
        self.app.post('/api/v1/auth/businesses',
                      data=json.dumps(self.data4), content_type='application/json')
        response = self.app.post(
            '/api/v1/auth/1/reviews', data=json.dumps(self.data), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["Unauthorised"], "Please login first")
        self.assertEqual(response.status_code, 401)

    def test_add_reviews(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data3), content_type='application/json')
        self.app.post('/api/v1/auth/login', data=json.dumps(self.data3),
                      content_type='application/json')
        self.app.post('/api/v1/auth/businesses',
                      data=json.dumps(self.data4), content_type='application/json')
        response = self.app.post(
            '/api/v1/auth/1/reviews', data=json.dumps(self.data), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review added Successfully")
        self.assertEqual(response.status_code, 201)

    def test_add_reviews_for_unavailable_business(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data3), content_type='application/json')
        self.app.post('/api/v1/auth/login', data=json.dumps(self.data3),
                      content_type='application/json')
        self.app.post('/api/v1/auth/businesses',
                      data=json.dumps(self.data4), content_type='application/json')
        response = self.app.post(
            '/api/v1/auth/2/reviews', data=json.dumps(self.data), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "Business with that ID does not exist")
        self.assertEqual(response.status_code, 404)

    def test_available_reviews(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data3), content_type='application/json')
        self.app.post('/api/v1/auth/login', data=json.dumps(self.data3),
                      content_type='application/json')
        self.app.post('/api/v1/auth/businesses',
                      data=json.dumps(self.data4), content_type='application/json')
        self.app.post('/api/v1/auth/1/reviews',
                      data=json.dumps(self.data), content_type='application/json')
        response = self.app.get(
            '/api/v1/auth/1/reviews', data=json.dumps(self.data), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data["description"],
                      result['Reviews']['description'])
        self.assertEqual(response.status_code, 200)

    def test_unvailable_reviews(self):
        self.app.post('/api/v1/auth/register',
                      data=json.dumps(self.data3), content_type='application/json')
        self.app.post('/api/v1/auth/login', data=json.dumps(self.data3),
                      content_type='application/json')
        self.app.post('/api/v1/auth/businesses',
                      data=json.dumps(self.data4), content_type='application/json')
        response = self.app.get('/api/v1/auth/2/reviews',
                                content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "No Reviews available")
        self.assertEqual(response.status_code, 404)
