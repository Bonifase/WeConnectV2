user_data = {
    "username": "username",
    "email": "user@gmail.com",
    "password": "user123"}
username_key_missing = dict(password="123we")
email_key_missing = dict(password="user123")
missing_password_key = dict(email="user@gmail.com")
invalid_username = dict(
    username=",",
    email="test@gmail.com",
    password="test123")
invalid_email = dict(username="username", email="hfgf", password="user234")
non_string_username = dict(
    username=2,
    email="username@gmail.com",
    password="user23")
no_string_email = dict(username="username", email=1, password="user345")
non_string_password = dict(
    username="username",
    email="username@gmail.com",
    password=1)
invalid_password = dict(
    username="user123",
    password=".",
    email="user123@gmail.com")
new_user = dict(username="Bill", email="bill@gmail.com", password="123456")
duplicate_user = dict(
    username="username",
    email="user@gmail.com",
    password="user123")
wrong_email = dict(email="user3@gmail.com", password="user123")
empty_login = dict(email="", password="")
unregistered_user = dict(
    email="notregistered@email.com",
    username="someuser",
    password="someuser123")
unavailable_username = dict(
    email="someuser@email.com",
    password="someuser123")
unavailable_email = dict(
    password="somepassword")
reset_password = dict(
    email="user@gmail.com", newpassword="user234")
confirm_password = dict(
    new_password="user234")
business_data = {
    "name": "easyE",
    "category": "hardware",
    "location": "Mombasa",
    "description": "Selling hardware products"}
short_business_name = {
    "name": "l",
    "category": "hardware",
    "location": "Mombasa",
    "description": "Selling hardware products"}
integer_business_name = dict(
    name=1,
    category="hardware",
    location="Mombasa",
    description="Selling hardware products")
empty_business_name = dict(
    name="2",
    category="hardware",
    location="Mombasa",
    description="Selling hardware products")
missing_business_key_name = dict(
    category="hardware", 
    location="Mombasa", 
    description="Selling hardware products")
invalid_business_location = {
    "name": "easy",
    "category": "hardware",
    "location": 1,
    "description": "Selling hardware products"}
new_business = dict(
    name="Texas ltd", 
    category="hardware", 
    location="Mombasa", 
    description="Selling hardware products")
unavailable_businesses = dict(
    name="Universal",
    category="hardware",
    location="Mombasa",
    description="Selling hardware products")
review_data = dict(description="This is an awesome business")
short_review_data = dict(description="")
