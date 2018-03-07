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
        print('app', self.app)
        self.data = {"username":"john", "email":"email@gmail.com","password":"12345"}
       
        

    def test_register_user(self):
        response = self.app.post('/v1/register_user', data = json.dumps(self.data) , content_type = 'application/json')
        rs = json.loads(response.data.decode())
        self.assertEqual(rs["message"], "Registered Successful")
        self.assertEqual(response.status_code, 201)
        
   
    


if __name__ == '__main__':
    unittest.main()
