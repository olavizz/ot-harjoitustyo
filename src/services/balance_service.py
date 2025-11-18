class BalanceService:

    def __init__(self, balance=0):
        self._balance = str(balance)
    
    def increase_balance(self, increment):
        value = self._balance
        self._balance = str(int(value) + int(increment))
        return self._balance
    
    def decrease_balance(self, decrement):
        value = self._balance
        self._balance = str(int(value) - int(decrement))
        return self._balance
    
    def _get_balance(self):
        return self._balance

balance_service = BalanceService()