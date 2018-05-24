import re


"""A method that checks username and business name patterns"""


def name_pattern(value):
    pattern = r'[a-zA-Z]{3,8}'
    match = re.search(pattern, value)
    return match
"""A method that checks email patterns"""


def email_pattern(value):
    pattern = r'[a-zA-Z0-9_\.&-]{4,30}@[a-z]+\..'
    match = re.search(pattern, value)
    return match
"""A method that checks password patterns"""


def password_pattern(value):

    pattern = r'[a-zA-Z0-9_@&\.]{6,20}'
    match = re.search(pattern, value)
    return match
"""A method that checks business location and description patterns"""


def attribute_pattern(value):
    pattern = r'[a-zA-Z]{2,8}'
    match = re.search(pattern, value)
    return match
    