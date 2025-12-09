import sqlite3

from services.balance_service import balance_service

DB_FILE = "src/budget.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


class ExpensesService:
    def __init__(self):
        self._expenses_list = []
        self._expenses = "0"

    def _add_expense(self, new_expense, new_expense_price, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO expenses (user_id, description, amount) VALUES (?, ?, ?)",
                (user_id, new_expense, new_expense_price),
            )
            print("Expense added successfully")

        except:
            print("Error adding expense")

        conn.commit()
        conn.close()

        self._update_balance_in_balance_service(new_expense_price, user_id)

    def _get_expenses(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT description, amount FROM expenses WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchall()
        except:
            print("get expenses function error")
            row = None

        if row is None:
            return 0

        conn.commit()
        conn.close()

        print(row, "This is row in get expenses")

        return row

    def _get_expenses_amount(self):
        return self._expenses

    def _update_balance_in_balance_service(self, decrement, user_id):
        balance_service.decrease_balance(decrement, user_id)
        return


expenses_service = ExpensesService()
