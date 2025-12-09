import sqlite3
import unittest

from services.expenses_service import ExpensesService

DB_FILE = "src/budget.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


test_user_id = 222
test_username = "pasi"
test_password = "kuikka"


class TestExpensesService(unittest.TestCase):
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

        self._expense = ExpensesService()

    def test_expenses_service_returns_list_of_expenses(self):
        self._expense._add_expense("car", 2000, test_user_id)
        self._expense._add_expense("lamp", 50, test_user_id)
        self.assertEqual(type(self._expense._get_expenses(test_user_id)), list)
