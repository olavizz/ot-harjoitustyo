import sqlite3

DB_FILE = "src/budget.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


class BalanceService:
    def __init__(self):
        self._balance = 0
        self._balance_var = 0
        self._total_earnings = 0

    def attach_vars(self, balance_var, total_earnings_var):
        self._balance_var = balance_var
        self._total_earnings_var = total_earnings_var

    def increase_balance(self, increment, user_id):
        value = int(self._get_balance(user_id))
        self._balance = str(value + int(increment))
        total_earnings = self._get_earnings(user_id) + int(increment)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE balances SET balance = ?, total_earnings = ? WHERE user_id = ?",
                (self._balance, total_earnings, user_id),
            )

        except:
            print("Error in updating balance")

        conn.commit()
        conn.close()

        self._total_earnings = str(int(self._total_earnings) + int(increment))
        return [self._balance, self._total_earnings]

    def decrease_balance(self, decrement, user_id):
        value = int(self._get_balance(user_id))
        print(value, "This is value in decrease balance")
        self._balance = str(value - int(decrement))

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE balances SET balance = ? WHERE user_id = ?",
                (self._balance, user_id),
            )
            print("decrease function works")
        except:
            print("Error in updating balance")

        conn.commit()
        conn.close()

        # self._balance_var.set(self._balance)

        return self._balance

    def _get_balance(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT balance FROM balances WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            print(row, "get balance function works")
        except Exception as e:
            print("get balance function error:", e)
            row = None

        conn.close()

        if row is None:
            return 0
        print(int(row[0]), "This is int(row[0]) in get balance function")
        return int(row[0])

    def init_user(self, user_id):
        self._balance = self._get_balance(user_id)
        self._total_earnings = self._get_earnings(user_id)

        if self._balance_var:
            self._balance_var.set(str(self._balance))

        if self._total_earnings:
            self._total_earnings_var.set(str(self._total_earnings))

    def _get_earnings(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT total_earnings FROM balances WHERE user_id = ?", (user_id,)
            )
            row = cursor.fetchone()
            print(row, "this is total earnings in get earnings function")

        except:
            print("Error fetching total earnings")
            row = None

        conn.commit()
        conn.close()
        if row is None:
            return 0
        print(row, "This is get earnings row")
        return int(row[0])


balance_service = BalanceService()
