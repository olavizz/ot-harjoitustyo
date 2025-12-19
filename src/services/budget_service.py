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
        # read current balance from DB to avoid stale cache
        current = self._get_balance_db(user_id)
        try:
            add_val = float(amount)
        except Exception:
            add_val = 0.0
        new_balance = current + add_val

        # ensure total_earnings uses floats consistently
        total_earnings = self._get_total_earnings(user_id) + add_val

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

        # update caches with float values
        self._cached_balance[user_id] = new_balance
        self._cached_earnings[user_id] = total_earnings

        return new_balance, total_earnings

    def decrease_balance(self, amount, user_id):
        # read current balance from DB to avoid stale cache
        current = self._get_balance_db(user_id)
        try:
            sub_val = float(amount)
        except Exception:
            sub_val = 0.0
        new_balance = current - sub_val

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

        # update cache with float value
        self._cached_balance[user_id] = new_balance

        return new_balance

    def _get_balance(self, user_id):
        # Return cached balance if present; ensure stored as float
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

        # store and return as float to avoid integer truncation issues
        balance = float(row[0]) if row and row[0] is not None else 0.0
        self._cached_balance[user_id] = balance
        return balance

    def _get_balance_db(self, user_id):
        """Read the balance directly from the database without using the cache."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT balance FROM balances WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
        except Exception as e:
            print("Error fetching balance from DB:", e)
            row = None
        conn.close()

        return float(row[0]) if row and row[0] is not None else 0.0

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

        # use float for total earnings to avoid truncation
        try:
            earnings = float(row[0]) if row and row[0] is not None else 0.0
        except Exception:
            earnings = 0.0
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

        try:
            amount = float(row[0]) if row and row[0] is not None else 0.0
        except Exception:
            amount = 0.0
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
        """Delete an expense by id and refund the amount to balance."""
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

            # read current balance directly from DB to avoid cache staleness
            current_balance = self._get_balance_db(user_id)
            try:
                amt = float(amount)
            except Exception:
                try:
                    amt = int(amount)
                except Exception:
                    amt = 0.0

            new_balance = current_balance + amt

            try:
                cursor.execute(
                    "UPDATE balances SET balance = ? WHERE user_id = ?",
                    (new_balance, user_id),
                )
            except Exception as e:
                print("Error updating balance after deleting expense:", e)

            conn.commit()
            conn.close()

            # update cache with float value
            self._cached_balance[user_id] = new_balance

            return True
        except Exception as e:
            print("Error deleting expense:", e)
            conn.close()
            return False

    def edit_expense(self, expense_id, user_id, new_description, new_amount):
        """Edit an expense's description and/or amount, and adjust balance accordingly.

        If the expense doesn't belong to the user, returns False.
        Returns True on success, False on error.
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Fetch current expense amount to compute delta
            cursor.execute(
                "SELECT amount FROM expenses WHERE id = ? AND user_id = ?",
                (expense_id, user_id),
            )
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False

            old_amount = row[0]

            # Parse numeric values robustly as floats
            try:
                old_val = float(old_amount)
            except Exception:
                try:
                    old_val = int(old_amount)
                    old_val = float(old_val)
                except Exception:
                    old_val = 0.0

            try:
                new_val = float(new_amount)
            except Exception:
                try:
                    new_val = int(new_amount)
                    new_val = float(new_val)
                except Exception:
                    new_val = 0.0

            delta = new_val - old_val

            # Update the expense row first
            try:
                cursor.execute(
                    "UPDATE expenses SET description = ?, amount = ? WHERE id = ? AND user_id = ?",
                    (new_description, new_amount, expense_id, user_id),
                )
            except Exception as e:
                print("Error updating expense row:", e)
                conn.close()
                return False

            # Always compute balances from DB to avoid cache inconsistencies
            current_balance_db = self._get_balance_db(user_id)

            # Since expenses reduce the available balance, increasing an expense should
            # decrease the balance by delta, while decreasing an expense should refund -delta.
            # So new_balance = current_balance_db - delta
            try:
                new_balance = current_balance_db - delta
            except Exception:
                new_balance = current_balance_db

            try:
                cursor.execute(
                    "UPDATE balances SET balance = ? WHERE user_id = ?",
                    (new_balance, user_id),
                )
            except Exception as e:
                print("Error updating balance after editing expense:", e)
                conn.close()
                return False

            conn.commit()
            conn.close()

            # Update cache with float value
            self._cached_balance[user_id] = new_balance

            return True

        except Exception as e:
            print("Error editing expense:", e)
            conn.close()
            return False


budget_service = BudgetService()
