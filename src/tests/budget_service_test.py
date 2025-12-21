import os
import sqlite3
import unittest

from repositories.budget_repository import BudgetRepository
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
        except sqlite3.Error as exc:
            # be explicit about the exception type to avoid bare except
            print("Error in test setup", exc)

        self.conn.commit()
        self.conn.close()

        self.balance = BudgetService()
        self.balance_repo = BudgetRepository()

    def test_balance_is_zero_at_start(self):
        self.assertEqual(self.balance._get_balance(test_user_id), 0)

    def test_balance_is_increased_right(self):
        self.balance.increase_balance(1000, test_user_id)
        self.assertEqual(self.balance._get_balance(test_user_id), 1000)

    def test_balance_is_decreased_right(self):
        self.balance.decrease_balance(1000, test_user_id)
        self.assertEqual(self.balance._get_balance(test_user_id), -1000)

    def test_total_earnings_is_right(self):
        self.balance.increase_balance(2000, test_user_id)
        self.balance.increase_balance(1500, test_user_id)
        self.balance.decrease_balance(500, test_user_id)
        self.assertEqual(self.balance._get_total_earnings(test_user_id), 3500)

    def test_add_expense_right(self):
        self.balance.add_expense("auto", "10000", "222")
        self.balance.add_expense("ruoka", "150", "222")
        self.balance.add_expense("bensa", "100", "222")
        self.assertEqual(len(self.balance.get_expenses(test_user_id)), 3)

    def test_delete_expense_right(self):
        self.balance.add_expense("auto", "10000", test_user_id)
        self.balance.add_expense("ruoka", "150", test_user_id)
        id = self.balance.add_expense("bensa", "100", test_user_id)
        self.balance.delete_expense(id, test_user_id)
        self.assertEqual(len(self.balance.get_expenses(test_user_id)), 2)

    def test_edit_expense_right(self):
        id1 = self.balance.add_expense("ravintola", "100", test_user_id)
        self.balance.edit_expense(
            id1, test_user_id, "ravintola Onnellinen Kana", "97.5"
        )
        expense = self.balance_repo.get_expense_by_id(id1)
        self.assertEqual(
            (expense[0], expense[1], expense[2], expense[3]),
            (id1, test_user_id, "ravintola Onnellinen Kana", 97.5),
        )
