import unittest
import json
from flask import jsonify
from tests import BaseTestSetUp, TestHelper
from tests.data import *


class TestBusinessCase(BaseTestSetUp):

    def test_get_all_business_list_works(self):
        """Test API can get all businesses (GET request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.get_businesses()
        result = json.loads(response.data.decode())
        self.assertIn(business_data['name'], result['businesses'][0]['1'][0])
        self.assertEqual(response.status_code, 200)

    def test_create_existing_business_fails(self):
        """Test API rejectsbusiness with existing name (POST request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.create_business(
            business_data=business_data, token=self.token)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['error'], "Business already Exist, use another name")
        self.assertEqual(response.status_code, 409)

    def test_short_business_name_does_not_work(self):
        """Test API can only createvalid business name that is not too short (POST request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        response = self.testHelper.create_business(
            business_data=short_business_name, token=self.token)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)

    def test_integer_business_name_does_not_work(self):
        """Test API rejects integer business name (POST request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        response = self.testHelper.create_business(
            business_data=integer_business_name, token=self.token)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)

    def test_empty_business_name_fails(self):
        """Test API rejects an empty business name (POST request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        response = self.testHelper.create_business(
            business_data=empty_business_name, token=self.token)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)

    def test_missing_business_key_name_doesnt_work(self):
        """Test API rejects missing key for business name (POST request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        response = self.testHelper.create_business(
            business_data=missing_business_key_name, token=self.token)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "name key is missing")
        self.assertEqual(response.status_code, 409)

    def test_create_new_business_works(self):
        """Test API creates a new business (POST request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        response = self.testHelper.create_business(
            business_data=new_business, token=self.token)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["message"], "You created this business")
        self.assertEqual(response.status_code, 201)

    def test_view_businesses_by_id(self):
        """Test API retrieves a businesses by it's ID (GET request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.get_business_by_id(businessid=1)
        result = json.loads(response.data.decode())
        self.assertIn(
            business_data['name'], result['business']['Business Name'])
        self.assertEqual(response.status_code, 200)

    def test_update_unavailable_businesses_fails(self):
        """Test API rjects update a businesses that isnt available (PUT request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.update_business(
            update_data=new_business, token=self.token, businessid=2)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Business not available")
        self.assertEqual(response.status_code, 404)

    def test_update_business_works(self):
        """Test API can update a businesses (PUT request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.update_business(
            update_data=new_business, token=self.token, businessid=1)
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business Updated")
        self.assertEqual(response.status_code, 201)

    def test_update_unavailable_business(self):
        """Test API cannot update a businesses unregistered (PUT request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        response = self.testHelper.update_business(
            update_data=new_business, token=self.token, businessid=100)
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business not available")
        self.assertEqual(response.status_code, 404)

    def test_update_with_available_name_fails(self):
        """Test API cannot update a businesses with business name that already exist (PUT request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.update_business(
            update_data=business_data, token=self.token, businessid=1)
        result = json.loads(response.data.decode())
        self.assertIn(result["error"],
                      "Business already Exist, use another name")
        self.assertEqual(response.status_code, 409)

    def test_update_with_invalid_name_fails(self):
        """Test API rejects update a businesses invalid business name (PUT request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.update_business(
            update_data=empty_business_name, token=self.token, businessid=1)
        result = json.loads(response.data.decode())
        self.assertIn(result["error"], "Invalid name")
        self.assertEqual(response.status_code, 409)

    def test_update_with_invalid_location_fails(self):
        """Test API cannot update a businesses with invalid business location (PUT request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.update_business(
            update_data=invalid_business_location, 
            token=self.token, businessid=1)
        result = json.loads(response.data.decode())
        self.assertIn(result["error"], "Invalid location")
        self.assertEqual(response.status_code, 409)

    def test_delete_business_works(self):
        """Test API can delete a businesses (DELETE request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.delete_business(
            businessid=1, token=self.token)
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "Business deleted")
        self.assertEqual(response.status_code, 200)

    def test_delete_unavailable_business_fails(self):
        """Test API cannot delete a businesses that is not available (DELETE request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        response = self.testHelper.delete_business(
            businessid=3, token=self.token)
        result = json.loads(response.data.decode())
        self.assertIn(result["message"], "No such Business")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
