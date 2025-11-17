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
    
    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._balance_var = StringVar()
        self._balance_var.set("0")
        self._expenses_var = StringVar()
        self._expenses_var.set("0")

        balance = ttk.Label(master=self._frame, text="balance", font=(20))
        expenses = ttk.Label(master=self._frame, text="expenses", font=(20))

        balance_amount = ttk.Label(master=self._frame, textvariable=self._balance_var)
        expenses_amount = ttk.Label(master=self._frame, textvariable=self._expenses_var)

        balance.grid(row=0, column=0, sticky=constants.W, padx=10)
        balance_amount.grid(row=0, column=1, sticky=constants.W, padx=10)
        expenses.grid(row=1, column=0, sticky=constants.W, padx=10)
        expenses_amount.grid(row=1, column=1, sticky=constants.W, padx=10)

    def dashboard(self):
        pass