class LoginService:
    def __init__(self):
        self._username = "pekka"
        self._password = "123456"
    
    def _check_user(self, username, password):
        if username == self._username and password == self._password:
            return True
        else:
            return False
    
login_service = LoginService()