import sqlite3

DB_FILE = "src/budget.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


class BudgetService:
    def __init__(self):
        self._cached_balance = {}
        self._cached_earnings = {}

    def increase_balance(self, amount, user_id):
        current = self._get_balance(user_id)
        new_balance = current + int(amount)

        total_earnings = self._get_total_earnings(user_id) + int(amount)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE balances SET balance = ?, total_earnings = ? WHERE user_id = ?",
                (new_balance, total_earnings, user_id),
            )
        except Exception as e:
            print("Error increasing balance:", e)

        conn.commit()
        conn.close()

        self._cached_balance[user_id] = new_balance
        self._cached_earnings[user_id] = total_earnings

        return new_balance, total_earnings

    def decrease_balance(self, amount, user_id):
        current = self._get_balance(user_id)
        new_balance = current - int(amount)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE balances SET balance = ? WHERE user_id = ?",
                (new_balance, user_id),
            )
        except Exception as e:
            print("Error decreasing balance:", e)

        conn.commit()
        conn.close()

        self._cached_balance[user_id] = new_balance

        return new_balance

    def _get_balance(self, user_id):
        if user_id in self._cached_balance:
            return self._cached_balance[user_id]

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT balance FROM balances WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
        except Exception as e:
            print("Error fetching balance:", e)
            row = None

        conn.close()

        balance = int(row[0]) if row else 0
        self._cached_balance[user_id] = balance
        return balance

    def get_balance(self, user_id):
        return self._get_balance(user_id)

    def _get_total_earnings(self, user_id):
        if user_id in self._cached_earnings:
            return self._cached_earnings[user_id]

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT total_earnings FROM balances WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
        except Exception as e:
            print("Error fetching total earnings:", e)
            row = None

        conn.close()

        earnings = int(row[0]) if row else 0
        self._cached_earnings[user_id] = earnings
        return earnings

    def add_expense(self, description, amount, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO expenses (user_id, description, amount) VALUES (?, ?, ?)",
                (user_id, description, amount),
            )
        except Exception as e:
            print("Error adding expense:", e)

        conn.commit()
        conn.close()

        self.decrease_balance(amount, user_id)

    def get_expenses_amount(self, user_id):
        """Return the total sum of expenses for the given user_id."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT SUM(amount) FROM expenses WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
        except Exception as e:
            print("Error getting expenses amount:", e)
            row = None

        conn.close()

        amount = int(row[0]) if row and row[0] is not None else 0
        return amount

    def get_expenses(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, description, amount FROM expenses WHERE user_id = ?",
                (user_id,),
            )
            rows = cursor.fetchall()
        except Exception as e:
            print("Error getting expenses:", e)
            rows = []

        conn.close()

        return rows

    def delete_expense(self, expense_id, user_id):
        """Delete an expense by id for the given user and refund the amount to balance."""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT amount FROM expenses WHERE id = ? AND user_id = ?",
                (expense_id, user_id),
            )
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False

            amount = row[0]

            cursor.execute(
                "DELETE FROM expenses WHERE id = ? AND user_id = ?",
                (expense_id, user_id),
            )

            current_balance = self._get_balance(user_id)
            try:
                new_balance = current_balance + int(amount)
            except Exception:
                new_balance = current_balance + float(amount)

            try:
                cursor.execute(
                    "UPDATE balances SET balance = ? WHERE user_id = ?",
                    (new_balance, user_id),
                )
            except Exception as e:
                print("Error updating balance after deleting expense:", e)

            conn.commit()
            conn.close()

            self._cached_balance[user_id] = int(new_balance)

            return True
        except Exception as e:
            print("Error deleting expense:", e)
            conn.close()
            return False


budget_service = BudgetService()
