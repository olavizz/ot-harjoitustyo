from tkinter import ttk, constants, StringVar
from services.expenses_service import expenses_service

class ExpensesView:
    def __init__(self, root):
        self._root = root
        self._expenses_var = None
        self._frame = None
        
        self._initialize()
    
    def pack(self):
        self._frame.grid(row=0, column=0)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._create_widgets()
        self._layout_widgets()
    
    def _create_widgets(self):
        self._expenses_view = ttk.Frame(master=self._frame)

        self._new_expense = ttk.Label(master=self._frame, text="Add a new expense", font=(30))
        self._expense_name = ttk.Label(master=self._frame, text="product or servide,", font=(20))
        self._expense_price = ttk.Label(master=self._frame, text="price €", font=(20))
        self._expense_ps_entry = ttk.Entry(master=self._frame)
        self._expense_price_entry = ttk.Entry(master=self._frame)
        self._expense_entry_button = ttk.Button(master=self._frame, text="Enter", command=self._add_expense)
        self._new_expense_amount = ttk.Entry(master=self._frame)
    
    def _layout_widgets(self):
        self._new_expense.grid(row=3, column=0, sticky=constants.W, padx=10, pady=10)
        self._expense_name.grid(row=4, column=0, sticky=constants.W, padx=10, pady=10)
        self._expense_ps_entry.grid(row=4, column=1, sticky=constants.W, padx=10 ,pady=10)
        self._expense_price.grid(row=5, column=0, sticky=constants.W, padx=10)
        self._expense_price_entry.grid(row=5, column=1, sticky=constants.W, padx=10)
        self._expense_entry_button.grid(row=6, column=1, sticky=constants.W, padx=10)
    
    def _add_expense(self):
        new_expense = self._expense_ps_entry.get()
        new_expense_price = self._expense_price_entry.get()

        expenses_service._add_expense(new_expense, new_expense_price)

        self._show_expenses()
    
    def _show_expenses(self):
        
        expenses_list = expenses_service._get_expenses()

        for i, name in enumerate(expenses_list):

            product = ttk.Label(master=self._expenses_view, text=name[0], font=(20))
            product.grid(row=i, column=0, sticky=constants.W, padx=10, pady=5)

            price = ttk.Label(master=self._expenses_view, text=name[1], font=(20))
            price.grid(row=i, column=1, sticky=constants.W, padx=10, pady=5)

        self._expenses_view.grid(row=7, column=0, sticky=constants.W, padx=10)