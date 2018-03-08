class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def reset_password(self, resetpassword):
        self.password = resetpassword

    

