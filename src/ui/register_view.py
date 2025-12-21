from tkinter import constants, ttk

from services.auth_service import auth_service


class RegisterView:
    def __init__(self, root, login_page):
        self._root = root
        self._frame = ttk.Frame(root, padding=20)
        self._show_login_page = login_page

        ttk.Label(self._frame, text="Register", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        ttk.Label(self._frame, text="Username:").grid(row=1, column=0, sticky="w")
        self.username_entry = ttk.Entry(self._frame)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self._frame, text="Password:").grid(row=2, column=0, sticky="w")
        self.password_entry = ttk.Entry(self._frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        self.register_button = ttk.Button(
            self._frame, text="Register", command=self.register_user
        )
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.back_button = ttk.Button(
            self._frame, text="Back to login", command=self._show_login_page
        )
        self.back_button.grid(row=3, column=2)

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            print("Username or password error")
            return

        auth_service.register_user(username, password)

    def show(self):
        """Show the register frame in the UI."""
        self._frame.grid(row=0, column=0, sticky=constants.W)

    def hide(self):
        self._frame.grid_remove()

    def destroy(self):
        self._frame.destroy()
