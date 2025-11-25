from tkinter import ttk, constants, StringVar

class LoginView:
    def __init__(self, root, login_successful):
        self._root = root
    
        self._login_successful = login_successful

        self._frame = ttk.Frame(root)
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        self._headline = ttk.Label(self._frame, text="Give username and password to login")
        self._username = ttk.Label(self._frame, text="Username")
        self._password = ttk.Label(self._frame, text="Password")
        self._username_entry = ttk.Entry(self._frame)
        self._password_entry = ttk.Entry(self._frame)

        self._login_button = ttk.Button(self._frame, text="Login", command=self._check_user)

    def _layout_widgets(self):
        self._headline.grid(row=0, column=0, sticky=constants.W, padx=10, pady=10)
        self._username.grid(row=1, column=0, sticky=constants.W, padx=10, pady=10)
        self._username_entry.grid(row=1, column=1, sticky=constants.W, padx=10, pady=10)
        self._password.grid(row=2, column=0, sticky=constants.W, padx=10, pady=10)
        self._password_entry.grid(row=2, column=1, sticky=constants.W, padx=10, pady=10)

    def _check_user(self):
        pass
    
    def show(self):
        self._frame.grid(row=0, column=0, sticky=constants.W)

    def hide(self):
        self._frame.grid_remove()