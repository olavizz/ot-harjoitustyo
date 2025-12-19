from tkinter import StringVar, constants, ttk

from services.budget_service import budget_service


class BalanceView:
    def __init__(self, root, budget_service, start_callback):
        self._root = root
        self._user_id = None
        self._balance_var = StringVar()
        self._total_earnings_var = StringVar()
        self._frame = None

        self.login_page = start_callback
        self._service = budget_service

        self._initialize()

    def pack(self):
        self._frame.grid(row=0, column=0)

    def show(self):
        self._frame.grid(row=0, column=0)

    def destroy(self):
        self._frame.destroy()

    def hide(self):
        self._frame.grid_remove()

    def set_user_id(self, user_id):
        self._user_id = user_id
        self._update_vars()

    def init_user(self, user_id):
        self.set_user_id(user_id)

    def update_balance(self):
        self._update_vars()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        self._total_earnings_label = ttk.Label(
            master=self._frame, text="total earnings", font=(20)
        )
        self._total_earnings_amount = ttk.Label(
            master=self._frame, textvariable=self._total_earnings_var
        )
        self._balance_label = ttk.Label(master=self._frame, text="balance", font=(20))

        self._balance_entry = ttk.Entry(master=self._frame)

        self._balance_amount = ttk.Label(
            master=self._frame, textvariable=self._balance_var
        )

        self._increase_button = ttk.Button(
            master=self._frame, text="increase", command=self._increase_balance
        )
        self._decrease_button = ttk.Button(
            master=self._frame, text="decrease", command=self._decrease_balance
        )
        self._log_out_button = ttk.Button(
            master=self._frame, text="logout", command=self._log_out
        )

    def _layout_widgets(self):
        self._total_earnings_label.grid(row=0, column=0, sticky=constants.W, padx=10)
        self._total_earnings_amount.grid(row=0, column=1, sticky=constants.W, padx=10)

        self._balance_label.grid(row=1, column=0, sticky=constants.W, padx=10)
        self._balance_amount.grid(row=1, column=1, sticky=constants.W, padx=10)

        self._balance_entry.grid(row=2, column=0)
        self._increase_button.grid(row=2, column=1)
        self._decrease_button.grid(row=2, column=2)
        self._log_out_button.grid(row=0, column=3)

    def _update_vars(self):
        if self._user_id is None:
            return

        balance = self._service.get_balance(self._user_id)
        earnings = self._service._get_total_earnings(self._user_id)

        self._balance_var.set(str(balance))
        self._total_earnings_var.set(str(earnings))

    def _increase_balance(self):
        if self._user_id is None:
            return

        amount = self._balance_entry.get()
        if not amount or not amount.isdigit():
            return

        new_balance, new_earnings = self._service.increase_balance(
            amount, self._user_id
        )

        self._balance_var.set(str(new_balance))
        self._total_earnings_var.set(str(new_earnings))

    def _decrease_balance(self):
        if self._user_id is None:
            return

        amount = self._balance_entry.get()
        if not amount or not amount.isdigit():
            return
        new_balance = self._service.decrease_balance(amount, self._user_id)
        self._balance_var.set(str(new_balance))

    def _log_out(self):
        self.login_page()
