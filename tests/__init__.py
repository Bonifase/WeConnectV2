import unittest, json
from urllib.parse import urljoin
# from urlparse import urljoin
from app import app
from config import app_config

from app.models.models import *
from tests.data import *

class BaseTestSetUp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.app = app.test_client()
        self.testHelper = TestHelper()
        self.base_url = self.testHelper.base_url
        self.app = self.testHelper.app
        self.headers = self.testHelper.headers

        with app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

        self.testHelper.register_user(user_data)
        self.result = self.testHelper.login_user(user_data)
        self.token = json.loads(self.result.data.decode())['access_token']
        
        return self.token

class TestHelper():

    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'
        self.headers = {'content-type': 'application/json'}
        self.app = app.test_client()
    #Create a new user

    def register_user(self, user_data):
        url = self.base_url + '/api/v2/auth/register'
        result = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)
        return result
    # #Reset user password

    # def reset_password(self, user_data):
    #     url = self.base_url + '/api/v2/auth/reset-password'
    #     result = self.app.post(url, data=json.dumps(
    #         user_data), headers=self.headers)
    #     return result

    # def confirm_reset_password(self, user_data, token=None):
    #     url = self.base_url + '/api/v2/auth/reset-password/{}'.format(token)
    #     result = self.app.post(url, data=json.dumps(
    #         confirm_password), headers=self.headers)
    #     return result
    # #login a user

    def login_user(self, user_data):
        url = self.base_url + '/api/v2/auth/login'
        result = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)
        return result
    #logout a user

    def logout_user(self, token=None):
        url = self.base_url + '/api/v2/auth/logout'
        return self.app.post(
            url,
            headers={
                **self.headers,
                'Authorization': 'Bearer {}'.format(token)})
    #create a new business

    def create_business(self, business_data, token):
        url = self.base_url + '/api/v2/businesses'
        return self.app.post(
            url,
            data=json.dumps(business_data),
            headers={
                **self.headers,
                "Authorization": 'Bearer {}'.format(token)})
    #Retrieve all the available businesses

    def get_businesses(self):
        url = self.base_url + '/api/v2/businesses'
        return self.app.get(url)
    #method to get business by id

    def get_business_by_id(self, businessid):
        url = self.base_url + '/api/v2/businesses/{id}'.format(id=businessid)
        return self.app.get(url)

    def update_business(self, businessid, update_data, token):

        url = self.base_url + f'/api/v2/businesses/{businessid}'
        return self.app.put(
            url,
            data=json.dumps(update_data),
            headers={
                **self.headers,
                'authorization': 'Bearer {}'.format(token)})
    #method to delete business

    def delete_business(self, businessid, token):
        url = self.base_url + '/api/v2/businesses/{}'.format(businessid)
        return self.app.delete(
            url,
            headers={
                **self.headers,
                'Authorization': 'Bearer {}'.format(token)})
    #Add review to a business method

    def add_business_review(self, businessid, review_data, token):
        url = urljoin(self.base_url,'/api/v2/{id}/reviews'.format(id=str(businessid)))
        return self.app.post(
            url, data=json.dumps(review_data), headers={
                **self.headers, 'Authorization': 'Bearer {}'.format(token)})
    #get all the reviews of a particular business

    def rerieve_all_reviews(self, businessid):
        url = urljoin(self.base_url,'/api/v2/{id}/reviews'.format(id=str(businessid)))
        return self.app.get(url)

    def reset_password(self, reset_data):
        url = self.base_url + '/api/v2/auth/reset-password'
        return self.app.post(
            url,
            data=json.dumps(reset_data),
            headers=self.headers)

    def confirm_reset_password(self, reset_data, reset_token):
        url = self.base_url + '/api/v2/auth/reset-password/' + reset_token
        return self.app.post(
            url,
            data=json.dumps(reset_data),
            headers=self.headers)


