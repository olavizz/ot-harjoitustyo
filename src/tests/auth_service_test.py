import sqlite3
import unittest

from services.auth_service import AuthService

DB_FILE = "src/budget.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


test_user_id = 222
test_username = "Kalle"
test_password = "1234"


class TestLoginService(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM expenses")
        self.cursor.execute("DELETE FROM balances")
        self.cursor.execute("DELETE FROM users")

        try:
            self.cursor.execute(
                "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
                (test_user_id, test_username, test_password),
            )
            self.cursor.execute(
                "INSERT INTO balances (user_id, balance) VALUES (?, ?)",
                (test_user_id, 0),
            )
            print("User added")
        except:
            print("Error in test setup")

        self.conn.commit()
        self.conn.close()

        self.auth_service = AuthService()

    def test_login_with_correct_username_and_password(self):
        login = self.auth_service._check_user("Kalle", "1234")
        self.assertEqual(login, True)

    def test_registering_user_with_unique_username_and_password(self):
        self.auth_service.register_user("Pekka", "9999")
        success = self.auth_service._check_user("Pekka", "9999")
        self.assertEqual(success, True)

    def test_get_correct_user_id(self):
        user_id = self.auth_service.get_login_user_id("Kalle", "1234")
        self.assertEqual(user_id, 222)
