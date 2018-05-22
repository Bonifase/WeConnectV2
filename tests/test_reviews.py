
import unittest
import json
from tests import BaseTestSetUp, TestHelper

from tests.data import *


class TestReviewCase(BaseTestSetUp):


    def test_add_reviews_works(self):
      """Test API add a review for existing business (POST request)"""

      self.testHelper.register_user(user_data)
      self.result = self.testHelper.login_user(user_data)
      self.token = json.loads(self.result.data.decode())['access_token']
      self.testHelper.create_business(business_data=business_data, token=self.token)
      response = self.testHelper.add_business_review(review_data=review_data, businessid=1, token=self.token)
      result = json.loads(response.data.decode())
      self.assertEqual(result["message"], "Review added Successfully")
      self.assertEqual(response.status_code, 201)


    def test_add_reviews_for_unavailable_business_id_fails(self):
      """Test API rejects create a review for a business that does not exist(POST request)"""

      self.testHelper.register_user(user_data)
      self.result = self.testHelper.login_user(user_data)
      self.token = json.loads(self.result.data.decode())['access_token']
      self.testHelper.create_business(business_data=business_data, token=self.token)
      response = self.testHelper.add_business_review(review_data=review_data,token=self.token, businessid=2)
      result = json.loads(response.data.decode())
      self.assertEqual(result["message"],
                         "Business with that ID does not exist")
      self.assertEqual(response.status_code, 404)

    def test_available_reviews_works(self):
      """Test API retrieves all reviews of a business(GET request)"""

      self.testHelper.register_user(user_data)
      self.result = self.testHelper.login_user(user_data)
      self.token = json.loads(self.result.data.decode())['access_token']
      self.testHelper.create_business(business_data=business_data, token=self.token)
      self.testHelper.add_business_review(review_data=review_data, businessid=1,token=self.token)
      response = self.testHelper.rerieve_all_reviews(businessid=1)
      result = json.loads(response.data.decode())
        
      self.assertIn(review_data["description"], result["Reviews"][0]["1"][1])
      self.assertEqual(response.status_code, 200)

    def test_unvailable_reviews_fails(self):
      """Test API rejects retrieve a business review for non existant business (GET request)"""

      self.testHelper.register_user(user_data)
      self.result = self.testHelper.login_user(user_data)
      self.token = json.loads(self.result.data.decode())['access_token']
      self.testHelper.create_business(business_data=business_data, token=self.token)
      self.testHelper.add_business_review(review_data=review_data, businessid=1,token=self.token )
      response = self.testHelper.rerieve_all_reviews(businessid=3)
      result = json.loads(response.data.decode())
      self.assertEqual(result["message"],
                         "No Reviews available for that Business")
      self.assertEqual(response.status_code, 404)
