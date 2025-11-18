from services.balance_service import balance_service

class ExpensesService:

    def __init__(self):
        self._expenses_list = []

    def _add_expense(self, new_expense, new_expense_price):
        self._expenses_list.append((new_expense, new_expense_price))
        print(self._expenses_list)

        #balance_service.decrease_balance(new_expense_price)
    
    def _get_expenses(self):
        return self._expenses_list

expenses_service = ExpensesService()