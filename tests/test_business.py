from app import app, db
import unittest

import json
from flask import jsonify
from config import app_config

from app.models.models import Business



class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.app =app.test_client()
        self.data = { "name":"easyE", "category":"hardware", "location":"Mombasa", "description":"Selling hardware products" }
        self.data2 = { "name":"Dlink", "category":"software", "location":"Nairobi", "description":"Selling software products"}
        self.data3 = { "name":"Ecosoft", "category":"software", "location":"Nakuru", "description":"Selling software products"}
        self.data4 = {"username":"test", "email":"test@gmail.com","password":"test123"}
       
        with app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()
            #create default user
            self.app.post('/api/v2/auth/register', data = json.dumps(self.data4) , content_type = 'application/json')
            self.login_user = self.app.post('/api/v2/auth/login', data = json.dumps(self.data4), content_type = 'application/json')
            result = json.loads(self.login_user.data.decode())
            print("This is result", result)
            self.user_token = result['access_token']
            self.app.post('/api/v2/businesses',
                      data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')


            

    def test_get_all_business_list_works(self):
        
        response = self.app.get('/api/v2/businesses', headers= {'x-access-token':self.user_token},
                                content_type='application/json')
        result = json.loads(response.data.decode())
        
        self.assertIn(self.data['name'], result['businesses'][0]['1'][0])
        self.assertEqual(response.status_code, 200)

    def test_create_existing_business_fails(self):
        """Test API can create a business (POST request)"""

        response = self.app.post(
            '/api/v2/businesses', data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['error'], "Business already Exist, use another name")
        self.assertEqual(response.status_code, 409)

    def test_short_business_name_does_not_work(self):
        
        response = self.app.post(
            '/api/v2/businesses', data=json.dumps(dict(name="E", category="hardware", location="Mombasa", description="Selling hardware products" )),
            headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)

    def test_integer_business_name_does_not_work(self):
        
        response = self.app.post(
            '/api/v2/businesses', data=json.dumps(dict(name=1, category="hardware", location="Mombasa", description="Selling hardware products" )),
            headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)


    def test_empty_business_name(self):
        
        response = self.app.post(
            '/api/v2/businesses', data=json.dumps(dict(name="", category="hardware", location="Mombasa", description="Selling hardware products" )),
            headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)

    def test_missing_business_key_name_doesnt_work(self):
        
        response = self.app.post(
            '/api/v2/businesses', data=json.dumps(dict( category="hardware", location="Mombasa", description="Selling hardware products" )),
            headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "name key is missing")
        self.assertEqual(response.status_code, 409)

    def test_create_new_business_works(self):
        
        
        response = self.app.post(
            '/api/v2/businesses', data=json.dumps(dict(name="Texas ltd", category="hardware", location="Mombasa", description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        print("KEY ERROR", result)
        self.assertEqual(
            result["message"], "Available businesses")
        self.assertEqual(response.status_code, 201)

    def test_get_all_businesses_works(self):
        
        
        response = self.app.get(
            '/api/v2/businesses', data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data['name'], result['businesses'][0]['1'][0])
        self.assertEqual(response.status_code, 200)

    def test_view_businesses_by_id(self):

        response = self.app.get(
            '/api/v2/businesses/1/', headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(self.data['name'], result['business']['name'])
        self.assertEqual(response.status_code, 200)

    def test_update_unavailable_businesses_fails(self):
        
       
        response = self.app.put(
            '/api/v2/businesses/5', data=json.dumps(dict(name="Universal", category="hardware", location="Mombasa", 
                description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        print("RESULTSSSSSS",result)
        self.assertEqual(result['message'], "Business not available")
        self.assertEqual(response.status_code, 404)

    def test_update_business_works(self):
     
        response = self.app.put(
            '/api/v2/businesses/1',  data=json.dumps(dict(name="Andela", category="hardware", location="Mombasa", 
                description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business Updated")
        self.assertEqual(response.status_code, 201)


    def test_update_unavailable_business(self):
       
        response = self.app.put(
            '/api/v2/businesses/6',  data=json.dumps(dict(name="Andela", category="hardware", location="Mombasa", 
                description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business not available")
        self.assertEqual(response.status_code, 404)


    def test_update_with_available_name(self):
      
        response = self.app.put(
            '/api/v2/businesses/1',  data=json.dumps(dict(name="easyE", category="hardware", location="Mombasa", 
                description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["error"], "Business already Exist, use another name")
        self.assertEqual(response.status_code, 409)

    def test_update_with_invalid_name_fails(self):
        
        response = self.app.put(
            '/api/v2/businesses/1',  data=json.dumps(dict(name="A", category="hardware", location="Mombasa", 
                description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)

    # def test_update_with_invalid_category_fails(self):
        
    #     response = self.app.put(
    #         '/api/v2/businesses/1',  data=json.dumps(dict(name="Fox", category="u", location="Mombasa", 
    #             description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
    #     result = json.loads(response.data.decode())
    #     self.assertIn(result["message"], "Invalid category")
    #     self.assertEqual(response.status_code, 409)

    def test_update_with_invalid_location_fails(self):
        
        response = self.app.put(
            '/api/v2/businesses/1',  data=json.dumps(dict(name="Fox", category="hardware", location="q", 
                description="Selling hardware products" )), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["error"], "Invalid location")
        self.assertEqual(response.status_code, 409)

    def test_delete_business_works(self):
        
        response = self.app.delete('/api/v2/businesses/1', headers= {'x-access-token':self.user_token}, data = json.dumps(self.data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business deleted")
        self.assertEqual(response.status_code, 200)


    def test_delete_unavailable_business(self):
        
        response = self.app.delete(
            '/api/v2/businesses/2',  data=json.dumps(self.data), headers= {'x-access-token':self.user_token}, content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "No such Business")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()