import unittest
from services.login_service import LoginService

class TestLoginService(unittest.TestCase):
    def setUp(self):
        self.login = LoginService()
    
    def test_login_with_correct_username_and_password(self):
        login = self.login._check_user("pekka", "123456")
        self.assertEqual(login, True)