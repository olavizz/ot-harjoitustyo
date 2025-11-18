import unittest
from services.balance_service import BalanceService

class TestBalanceService(unittest.TestCase):
    def setUp(self):
        self.balance = BalanceService(0)

    def test_balance_is_zero_at_start(self):
        self.assertEqual(self.balance._get_balance(), "0")

    def test_balance_is_increased_right(self):
        self.balance.increase_balance(1000)
        self.assertEqual(self.balance._get_balance(), "1000")