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
        self.data = {"username":"john", "email":"email@gmail.com","password":"12345"}
        self.data2 = {"username":"Bill", "email":"bill@gmail.com","password":"12345"}
       
        

    def test_register_user(self):
        response = self.app.post('/v1/register_user', data = json.dumps(self.data) , content_type = 'application/json')
        rs = json.loads(response.data.decode())
        self.assertEqual(rs["message"], "Registered Successful")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_register(self):
        response1 = self.app.post('/v1/register_user', data = json.dumps(self.data2) , content_type = 'application/json')
        rs1 = json.loads(response1.data.decode())
        self.assertEqual(rs1["message"], "Registered Successful")
        self.assertEqual(response1.status_code, 201)
        response2 = self.app.post('/v1/register_user', data = json.dumps(self.data2) , content_type = 'application/json')
        rs2 = json.loads(response2.data.decode())
        self.assertEqual(rs2["message"], "User Details Exist")
        self.assertEqual(response2.status_code, 406)


        
   
    


if __name__ == '__main__':
    unittest.main()
