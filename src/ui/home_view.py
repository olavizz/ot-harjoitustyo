from tkinter import ttk, constants, StringVar

class HomeView:
    def __init__(self, root):
        self._root = root
        self._balance_var = None
        self._expenses_var = None
        self.expenses_list = []
        self._frame = None 
        self._service = HomeService()

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
        self._frame = ttk.Frame(master=self._root)

        self._balance = ttk.Label(master=self._frame, text="balance", font=(20))
        self._expenses = ttk.Label(master=self._frame, text="expenses", font=(20))
        self._balance_entry = ttk.Entry(master=self._frame)

        self._new_expense = ttk.Label(master=self._frame, text="Add a new expense", font=(30))
        self._expense_entry = ttk.Entry(master=self._frame)
        self._expense_entry_button = ttk.Button(master=self._frame, text="Enter", command=self._add_expense)

        self._balance_amount = ttk.Label(master=self._frame, textvariable=self._balance_var)
        self._expenses_amount = ttk.Label(master=self._frame, textvariable=self._expenses_var)
        self._increase_button = ttk.Button(master=self._frame, text="increase", command=self._increase_balance)
        self._decrease_button = ttk.Button(master=self._frame, text="decrease", command=self._decrease_balance)
    

    def _init_variables(self):
        self._balance_var = StringVar()
        self._balance_var.set("0")
        self._expenses_var = StringVar()
        self._expenses_var.set("0")
    
    def _layout_widgets(self):
        self._balance.grid(row=0, column=0, sticky=constants.W, padx=10)
        self._balance_amount.grid(row=0, column=1, sticky=constants.W, padx=10)
        self._expenses.grid(row=1, column=0, sticky=constants.W, padx=10)
        self._expenses_amount.grid(row=1, column=1, sticky=constants.W, padx=10)
        self._balance_entry.grid(row=2, column=0)
        self._increase_button.grid(row=2, column=1)
        self._decrease_button.grid(row=2, column=2)
        self._new_expense.grid(row=3, column=0, sticky=constants.W, padx=10, pady=10)
        self._expense_entry.grid(row=4, column=0, sticky=constants.W, padx=10 ,pady=10)
        self._expense_entry_button.grid(row=4, column=1, sticky=constants.W, padx=10)
    
    def _increase_balance(self):
        value = self._balance_var.get()
        increment = self._balance_entry.get()
        new_balance = self._service.increase_balance(value, increment)
        self._balance_var.set(str(new_balance))
    
    def _decrease_balance(self):
        value = self._balance_var.get()
        decrement = self._balance_entry.get()
        new_balance = self._service.decrease_balance(value, decrement)
        self._balance_var.set(str(new_balance))
    
    def _add_expense(self):
        #expense = self._expense_entry
        pass
    
    def _show_expenses(self):
        pass


class HomeService:
    
    def increase_balance(self, value, increment):
        return int(value) + int(increment)
    
    def decrease_balance(self, value, decrement):
        return int(value) - int(decrement)
    
    