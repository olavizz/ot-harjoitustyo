from tkinter import ttk, constants, StringVar

class HomeView:
    def __init__(self, root):
        self._root = root
        self._balance_var = None
        self._expenses_var = None
        self._frame = None 

        self._initialize()

    def pack(self):
        self._frame.grid(row=0, column=0)
    
    def destroy(self):
        self._frame.destroy()
    
    def _increase_balance(self):
        value = self._balance_var.get()
        increment = self._balance_entry.get()
        self._balance_var.set(str(int(value) + int(increment)))
    
    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._balance_var = StringVar()
        self._balance_var.set("0")
        self._expenses_var = StringVar()
        self._expenses_var.set("0")

        balance = ttk.Label(master=self._frame, text="balance", font=(20))
        expenses = ttk.Label(master=self._frame, text="expenses", font=(20))
        self._balance_entry = ttk.Entry(master=self._frame)

        balance_amount = ttk.Label(master=self._frame, textvariable=self._balance_var)
        expenses_amount = ttk.Label(master=self._frame, textvariable=self._expenses_var)
        increase_button = ttk.Button(master=self._frame, text="increase", command=self._increase_balance)

        balance.grid(row=0, column=0, sticky=constants.W, padx=10)
        balance_amount.grid(row=0, column=1, sticky=constants.W, padx=10)
        expenses.grid(row=1, column=0, sticky=constants.W, padx=10)
        expenses_amount.grid(row=1, column=1, sticky=constants.W, padx=10)
        self._balance_entry.grid(row=2, column=0)
        increase_button.grid(row=2, column=1)

    def dashboard(self):
        pass