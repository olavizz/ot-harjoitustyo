import sqlite3
DB_FILE = "src/budget.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

class LoginService:
    def __init__(self):
        self._username = "pekka"
        self._password = "123456"
    
    def get_login_user_id(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            print(user)
            print("User found")
        except sqlite3.Error as e:
            print("User not found")
        conn.close()
        return user[0]
    
    def _check_user(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            print(user)
            print("User found")
            self._username = user[1]
            self._password = user[2]
        except sqlite3.Error as e:
            print("Database error:", e)

        conn.close()

        if username == self._username and password == self._password:
            return True
        else:
            return False
    
login_service = LoginService()