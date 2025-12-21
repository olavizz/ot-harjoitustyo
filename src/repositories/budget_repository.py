import sqlite3

DB_FILE = "src/budget.db"


class BudgetRepository:
    def get_connection(self) -> sqlite3.Connection:
        """Create a new sqlite3 connection with foreign keys enabled."""
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def get_balance(self, user_id: int):
        """Return the user's balance as float. Returns 0.0 if missing."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance FROM balances WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row and row[0] is not None:
                return float(row[0])
            return 0.0
        except Exception as e:
            print("Error getting balance:", e)
            return 0.0
        finally:
            conn.close()

    def get_total_earnings(self, user_id: int):
        """Return the user's total_earnings as float. Returns 0.0 if missing."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT total_earnings FROM balances WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchone()
            if row and row[0] is not None:
                return float(row[0])
        except Exception as e:
            print("Error getting total_earnings:", e)

        conn.close()
        return 0.0

    def set_balance_and_earnings(
        self, user_id: int, balance: float, total_earnings: float
    ):
        """Set both balance and total_earnings. Returns True on success."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE balances SET balance = ?, total_earnings = ? WHERE user_id = ?",
                (float(balance), float(total_earnings), user_id),
            )
            conn.commit()
            return True
        except Exception as e:
            print("Error setting balance and earnings:", e)
            return False
        finally:
            conn.close()

    def update_balance(self, user_id: int, new_balance: float):
        """Set new balance value for user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE balances SET balance = ? WHERE user_id = ?",
                (float(new_balance), user_id),
            )
            conn.commit()
            return True
        except Exception as e:
            print("Error updating balance:", e)
            return False
        finally:
            conn.close()

    def update_total_earnings(self, user_id: int, new_total: float):
        """Set new total_earnings value for user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE balances SET total_earnings = ? WHERE user_id = ?",
                (float(new_total), user_id),
            )
            conn.commit()
            return True
        except Exception as e:
            print("Error updating total_earnings:", e)
            return False
        finally:
            conn.close()

    def add_expense(self, user_id: int, description: str, amount: float):
        """Add an expense row. Returns the created expense id or None on failure."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO expenses (user_id, amount, description) VALUES (?, ?, ?)",
                (user_id, float(amount), description),
            )
            expense_id = cursor.lastrowid
            conn.commit()
            return expense_id
        except Exception as e:
            print("Error adding expense:", e)
            return None
        finally:
            conn.close()

    def get_expenses_by_user(self, user_id: int):
        """Return list of (id, description, amount) for a given user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, description, amount FROM expenses WHERE user_id = ? ORDER BY id DESC",
                (user_id,),
            )
            rows = cursor.fetchall()
            # normalize types
            normalized = []
            for r in rows:
                eid = r[0]
                desc = r[1]
                amt = float(r[2]) if r[2] is not None else 0.0
                normalized.append((eid, desc, amt))
            return normalized
        except Exception as e:
            print("Error fetching expenses:", e)
            return []
        finally:
            conn.close()

    def get_expense_by_id(self, expense_id: int):
        """Return (id, user_id, description, amount) or None if not found."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, user_id, description, amount FROM expenses WHERE id = ?",
                (expense_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            return (
                row[0],
                row[1],
                row[2],
                float(row[3]) if row[3] is not None else 0.0,
            )
        except Exception as e:
            print("Error fetching expense by id:", e)
            return None
        finally:
            conn.close()

    def delete_expense(self, expense_id: int):
        """Delete an expense by id. Returns True if a row was deleted, False otherwise."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            affected = cursor.rowcount
            conn.commit()
            return affected > 0
        except Exception as e:
            print("Error deleting expense:", e)
            return False
        finally:
            conn.close()

    def update_expense(self, expense_id: int, description: str, amount: float):
        """Update an expense's description and amount. Returns True on success."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE expenses SET description = ?, amount = ? WHERE id = ?",
                (description, float(amount), expense_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error updating expense:", e)
            return False
        finally:
            conn.close()

    def get_total_expenses_amount(self, user_id: int):
        """Return amount for a user's expenses as float."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchone()
            if row and row[0] is not None:
                return float(row[0])
            return 0.0
        except Exception as e:
            print("Error getting total expenses amount:", e)
            return 0.0
        finally:
            conn.close()


budget_repository = BudgetRepository()
