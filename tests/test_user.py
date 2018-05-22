import unittest, json
from tests import BaseTestSetUp
from tests.data import *


class TestUserCase(BaseTestSetUp):  

    def test_missing_username_key_registration_fails(self):
        """Test API rejects username key that is missing (POST request)"""

        response = self.testHelper.register_user(unavailable_username)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "username key is missing")
        self.assertEqual(response.status_code, 409)

    def test_invalid_username_registration_fails(self):
        """Test API rejects invalid username registration (POST request)"""

        response = self.testHelper.register_user(invalid_username)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid username")
        self.assertEqual(response.status_code, 409)

    def test_invalid_email_registrartion_fails(self):
        """Test API rejects invalid password registration(POST request)"""

        response = self.testHelper.register_user(invalid_email)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid email")
        self.assertEqual(response.status_code, 409)

    def test_non_string_username_registrartion_fails(self):
        """Test API rejects non-string username registration (POST request)"""

        response = self.testHelper.register_user(non_string_username)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid username")
        self.assertEqual(response.status_code, 409)

    def test_no_string_email_registrartion_fails(self):
        """Test API rejects non-string email registration (POST request)"""

        response = self.testHelper.register_user(no_string_email)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "Invalid email")
        self.assertEqual(response.status_code, 409)

    def test_non_string_password_registrartion_fails(self):
        """Test API rejects non-string password registration (POST request)"""

        response = self.testHelper.register_user(non_string_password)
        result = json.loads(response.data.decode())
        
        self.assertEqual(result["error"], "Invalid password")
        self.assertEqual(response.status_code, 409)

    def test_invalid_password_registration(self):
        """Test API rejects invalid password registration (POST request)"""

        response = self.testHelper.register_user(invalid_password)
        result = json.loads(response.data.decode())
        
        self.assertEqual(result["error"], "Invalid password")
        self.assertEqual(response.status_code, 409)

    def test_new_user_registration_works(self):
        """Test API registers new user successfully (POST request)"""

        response = self.testHelper.register_user(new_user)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You registered successfully. Please log in")
        self.assertEqual(response.status_code, 201)

    def test_duplicate_user_registration_fails(self):
        """Test API rejects registration of a user email twice (POST request)"""
        
        self.testHelper.register_user(user_data)
        response2 = self.testHelper.register_user(user_data)
        result2 = json.loads(response2.data.decode())

        self.assertEqual(result2["message"], "User already exists. Please login")
        self.assertEqual(response2.status_code, 409)

    def test_user_login_works(self):
        """Test API logs in users successfully (POST request)"""

        self.testHelper.register_user(user_data)
        response = self.testHelper.login_user(user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You logged in successfully.")
        self.assertEqual(response.status_code, 200)

    def test_wrong_email_login_fails(self):
        """Test API rejects wrong email during login (POST request)"""

        response = self.testHelper.login_user(wrong_email)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid email, Please try again")
        self.assertEqual(response.status_code, 409)

    def test_missing_email_key_login_fails(self):
        """Test API rejects missing email key during login (POST request)"""

        response = self.testHelper.login_user(email_key_missing)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "email key is missing")
        self.assertEqual(response.status_code, 409)

    def test_missing_password_key_login_fails(self):
        """Test API rejects missing password key during login (POST request)"""

        response = self.testHelper.login_user(missing_password_key)
        result = json.loads(response.data.decode())
        self.assertEqual(result["error"], "password key is missing")
        self.assertEqual(response.status_code, 409)

    def test_empty_login_fails(self):
        """Test API rejects empty user details during login (POST request)"""

        response = self.testHelper.login_user(empty_login)
        result = json.loads(response.data.decode())
        self.assertTrue(result["message"], "Incomplete entry")
        self.assertEqual(response.status_code, 409)

    def test_unregistered_user_login_fails(self):
        """Test API rejects login requests from unregistered users (POST request)"""

        response = self.testHelper.login_user(unregistered_user)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid email, Please try again")
        self.assertEqual(response.status_code, 409)

    def test_unavailable_email_not_allowed(self):
        """Test API rejects reset password request from empty email (POST request)"""

        self.testHelper.register_user(user_data)
        response1 = self.testHelper.reset_password(unavailable_email)
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], "Please provide your email")
        self.assertEqual(response1.status_code, 409)

    def test_reset_user_password_works(self):
        """Test API reset user password works (POST request)"""

        self.testHelper.register_user(user_data)
        response1 = self.testHelper.reset_password(reset_data=reset_password)
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], 
            "Use this token to reset your password.")
        self.assertEqual(response1.status_code, 200)
        token = result1["reset_token"]
        response2 = self.testHelper.confirm_reset_password(
            reset_data=confirm_password,reset_token=token)
        result2 = json.loads(response2.data.decode())

        self.assertEqual(result2["message"], "password reset Successful")
        self.assertEqual(response2.status_code, 200)

    def test_invalid_reset_token_fails(self):
        """Test API reset user password works (POST request)"""

        self.testHelper.register_user(user_data)
        response1 = self.testHelper.reset_password(reset_data=reset_password)
        result1 = json.loads(response1.data.decode())
        self.assertEqual(result1["message"], 
            "Use this token to reset your password.")
        self.assertEqual(response1.status_code, 200)
        token = "bdvfugdygduywg"
        response2 = self.testHelper.confirm_reset_password(
            reset_data=confirm_password,reset_token=token)
        result2 = json.loads(response2.data.decode())

        self.assertEqual(result2["msg"], "Not enough segments")
        self.assertEqual(response2.status_code, 422)

    def test_reset_unregistered_user_password_fails(self):
        """Test API rejects reset password request from unregistered email (POST request)"""

        response = self.testHelper.reset_password(reset_data=unregistered_user)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User does not exixt, please register")


    