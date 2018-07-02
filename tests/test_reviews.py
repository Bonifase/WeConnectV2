
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
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.add_business_review(
            review_data=review_data, businessid=1, token=self.token)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Review added Successfully")
        self.assertEqual(response.status_code, 201)

    def test_add_reviews_for_unavailable_business_id_fails(self):
        """Test API reject add review for uncreated business(POST request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        response = self.testHelper.add_business_review(
            review_data=review_data, token=self.token, businessid=2)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"],
                         "Business with that ID does not exist")
        self.assertEqual(response.status_code, 404)

    def test_get_available_reviews_works(self):
        """Test API retrieves all reviews of a business(GET request)"""

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        self.testHelper.create_business(
            business_data=business_data, token=self.token)
        self.testHelper.add_business_review(
            review_data=review_data, businessid=1, token=self.token)
        response = self.testHelper.rerieve_all_reviews(businessid=1)
        result = json.loads(response.data.decode())

        self.assertIn(review_data["description"], result['Reviews'][0]['body'])
        self.assertEqual(response.status_code, 200)
