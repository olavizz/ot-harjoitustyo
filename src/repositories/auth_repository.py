import sqlite3

DB_FILE = "src/budget.db"


def get_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise


class AuthRepository:
    def get_user_id(self, username, password):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username = ? AND password = ?",
                (username, password),
            )
            user = cursor.fetchone()
            if user is None:
                return None
            return user[0]
        except sqlite3.Error as e:
            print(f"Database error in get_user_id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def username_exists(self, username):
        """Check whether a username already exists in the users table."""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM users WHERE username = ?",
                (username,),
            )
            user = cursor.fetchone()
            return user is not None
        except sqlite3.Error as e:
            print(f"Database error in username_exists: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def check_user(self, username, password):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM users WHERE username = ? AND password = ?",
                (username, password),
            )
            user = cursor.fetchone()
            return user is not None
        except sqlite3.Error as e:
            print(f"Database error in check_user: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def register_user(self, username, password):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO balances (user_id, balance) VALUES (?, ?)", (user_id, 0)
            )
            conn.commit()
            print("User added")
            return True
        except sqlite3.IntegrityError as e:
            if conn:
                conn.rollback()
            print(f"Integrity error in register_user (username may already exist): {e}")
            return False
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"Database error in register_user: {e}")
            return False
        finally:
            if conn:
                conn.close()


auth_repository = AuthRepository()
