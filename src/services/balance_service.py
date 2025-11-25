
class BalanceService:

    def __init__(self, balance=0):
        self._balance = str(balance)
        self._balance_var = None
        self._total_earnings = str(balance)

    def attach_vars(self, balance_var):
        self._balance_var = balance_var
        self._balance_var.set(str(self._balance))

    def increase_balance(self, increment):
        value = int(self._balance)
        self._balance = str(value + int(increment))
        self._total_earnings = (str(int(self._total_earnings) + int(increment)))
        return [self._balance, self._total_earnings]

    def decrease_balance(self, decrement):
        value = int(self._balance)
        self._balance = str(value - int(decrement))

        if self._balance_var:
            self._balance_var.set(str(self._balance))

        return self._balance

    def _get_balance(self):
        return self._balance
    
    def _get_earnings(self):
        return self._total_earnings

balance_service = BalanceService()
