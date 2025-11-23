from tkinter import ttk, constants, StringVar
from services.balance_service import balance_service

class BalanceView:
    def __init__(self, root):
        self._root = root
        self._balance_var = None
        self._total_earnings_var = None
        self._frame = None
        self._balance_service = balance_service
        self._balance_var = StringVar()
        self._total_earnings_var = StringVar()
        
        self._balance_service.attach_vars(self._balance_var)

        self._initialize()

    def pack(self):
        self._frame.grid(row=0, column=0)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._init_variables()
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        self._total_earnings = ttk.Label(master=self._frame, text="total earnings", font=(20))
        self._total_earnings_amount = ttk.Label(master=self._frame, textvariable=self._total_earnings_var)
        self._balance = ttk.Label(master=self._frame, text="balance", font=(20))
        self._balance_entry = ttk.Entry(master=self._frame)
        self._balance_amount = ttk.Label(master=self._frame, textvariable=self._balance_var)
        self._increase_button = ttk.Button(master=self._frame, text="increase", command=self._increase_balance)
        self._decrease_button = ttk.Button(master=self._frame, text="decrease", command=self._decrease_balance)

    def _init_variables(self):
        balance = balance_service._get_balance()
        total_earnings = balance_service._get_earnings()
        self._balance_var.set(balance)
        self._total_earnings_var.set(total_earnings)

    def _layout_widgets(self):
        self._total_earnings.grid(row=0, column=0, sticky=constants.W, padx=10)
        self._total_earnings_amount.grid(row=0, column=1, sticky=constants.W, padx=10)
        self._balance.grid(row=1, column=0, sticky=constants.W, padx=10)
        self._balance_amount.grid(row=1, column=1, sticky=constants.W, padx=10)
        self._balance_entry.grid(row=2, column=0)
        self._increase_button.grid(row=2, column=1)
        self._decrease_button.grid(row=2, column=2)

    def _increase_balance(self):
        increment = self._balance_entry.get()
        new_balance = balance_service.increase_balance(increment)
        self._balance_var.set(str(new_balance[0]))
        self._total_earnings_var.set(str(new_balance[1]))

    def _decrease_balance(self, subtraction=None):
        decrement = int(self._balance_entry.get())

        if subtraction == None:
            new_balance = balance_service.decrease_balance(decrement)
            self._balance_var.set(str(new_balance))
        else:
            subtraction = int(subtraction)
            new_balance = balance_service.decrease_balance(subtraction)
            self._balance_var.set(str(new_balance))
