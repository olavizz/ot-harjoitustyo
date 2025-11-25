import unittest
from services.expenses_service import ExpensesService

class TestExpensesService(unittest.TestCase):
    def setUp(self):
        self._expense = ExpensesService()

    def test_expenses_is_zero_at_start(self):
        self.assertEqual(self._expense._get_expenses_amount(), "0")

    def test_expenses_are_increased_right(self):
        self._expense._add_expense("car", 2000)
        self._expense._add_expense("lamp", 50)
        self.assertEqual(self._expense._get_expenses_amount(), "2050")
    
    def test_expenses_service_returns_list_of_expenses(self):
        self._expense._add_expense("car", 2000)
        self._expense._add_expense("lamp", 50)
        self.assertEqual(type(self._expense._get_expenses()), list)
        