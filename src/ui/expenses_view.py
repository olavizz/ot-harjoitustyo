from tkinter import StringVar, constants, ttk


class ExpensesView:
    def __init__(self, root, budget_service, update_balance):
        self._root = root
        self._budget_service = budget_service
        self._user_id = None
        self._expenses_var = StringVar()
        self._frame = None
        self._update_balance = update_balance

        self._initialize()

    def pack(self):
        self._frame.grid(row=0, column=0)

    def destroy(self):
        self._frame.destroy()

    def set_user_id(self, user_id):
        self._user_id = user_id

    def init_user(self, user_id):
        self._user_id = user_id
        self._init_variables()
        if (
            not hasattr(self, "_expenses_view")
            or not self._expenses_view.winfo_exists()
        ):
            self._expenses_view = ttk.Frame(master=self._frame)
        self._show_expenses()

    def _init_variables(self):
        amount = self._budget_service.get_expenses_amount(self._user_id)
        self._expenses_var.set(amount)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        self._expenses_view = ttk.Frame(master=self._frame)

        self._expenses = ttk.Label(master=self._frame, text="expenses", font=(20))
        self._expenses_amount = ttk.Label(
            master=self._frame, textvariable=self._expenses_var
        )

        self._new_expense = ttk.Label(
            master=self._frame, text="Add a new expense", font=(30)
        )

        self._expense_name = ttk.Label(
            master=self._frame, text="product or service", font=(20)
        )
        self._expense_price = ttk.Label(master=self._frame, text="price €", font=(20))

        self._expense_ps_entry = ttk.Entry(master=self._frame)
        self._expense_price_entry = ttk.Entry(master=self._frame)

        self._expense_entry_button = ttk.Button(
            master=self._frame, text="Enter", command=self._add_expense
        )

    def _layout_widgets(self):
        self._expenses.grid(row=1, column=0, sticky=constants.W, padx=10)
        self._expenses_amount.grid(row=1, column=1, sticky=constants.W, padx=10)
        self._new_expense.grid(row=3, column=0, sticky=constants.W, padx=10, pady=10)
        self._expense_name.grid(row=4, column=0, sticky=constants.W, padx=10, pady=10)
        self._expense_ps_entry.grid(
            row=4, column=1, sticky=constants.W, padx=10, pady=10
        )
        self._expense_price.grid(row=5, column=0, sticky=constants.W, padx=10)
        self._expense_price_entry.grid(row=5, column=1, sticky=constants.W, padx=10)
        self._expense_entry_button.grid(row=6, column=1, sticky=constants.W, padx=10)

    def _add_expense(self):
        name = self._expense_ps_entry.get()
        price = self._expense_price_entry.get()

        self._budget_service.add_expense(name, price, self._user_id)

        new_amount = self._budget_service.get_expenses_amount(self._user_id)
        self._expenses_var.set(new_amount)

        self._update_balance()
        self._show_expenses()

    def _delete_expense(self, expense_id):
        """Delete an expense and refresh the view & balance."""
        if self._user_id is None:
            return

        deleted = self._budget_service.delete_expense(expense_id, self._user_id)
        if deleted:
            new_amount = self._budget_service.get_expenses_amount(self._user_id)
            self._expenses_var.set(new_amount)
            self._update_balance()
            self._show_expenses()

    def _show_expenses(self):
        if (
            not hasattr(self, "_expenses_view")
            or not self._expenses_view.winfo_exists()
        ):
            self._expenses_view = ttk.Frame(master=self._frame)
        for widget in self._expenses_view.winfo_children():
            widget.destroy()

        if self._user_id is None:
            expenses_list = []
        else:
            expenses_list = self._budget_service.get_expenses(self._user_id)

        for i, row in enumerate(expenses_list):
            if len(row) == 3:
                expense_id, product_name, product_price = row
            elif len(row) == 2:
                expense_id = None
                product_name, product_price = row
            else:
                expense_id = None
                product_name = str(row)
                product_price = ""

            product = ttk.Label(
                master=self._expenses_view, text=product_name, font=(20)
            )
            product.grid(row=i, column=0, sticky=constants.W, padx=10, pady=5)

            price = ttk.Label(master=self._expenses_view, text=product_price, font=(20))
            price.grid(row=i, column=1, sticky=constants.W, padx=10, pady=5)

            if expense_id is not None:
                delete_btn = ttk.Button(
                    master=self._expenses_view,
                    text="Delete",
                    command=lambda eid=expense_id: self._delete_expense(eid),
                )
                delete_btn.grid(row=i, column=2, sticky=constants.W, padx=10, pady=5)

        self._expenses_view.grid(row=7, column=0, sticky=constants.W, padx=10)

    def hide(self):
        self._frame.grid_remove()
