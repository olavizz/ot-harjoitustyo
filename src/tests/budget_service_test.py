import os
import sqlite3
import unittest
from configparser import ParsingError

from services.budget_service import BudgetService

DB_FILE = "src/budget.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


test_user_id = 222
test_username = "Kalle"
test_password = "1234"


class TestBalanceService(unittest.TestCase):
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

        self.balance = BudgetService()

    def test_balance_is_zero_at_start(self):
        self.assertEqual(self.balance._get_balance(test_user_id), 0)

    def test_balance_is_increased_right(self):
        self.balance.increase_balance(1000, test_user_id)
        self.assertEqual(self.balance._get_balance(test_user_id), 1000)
