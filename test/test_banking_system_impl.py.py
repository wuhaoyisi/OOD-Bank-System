import unittest
from banking_system.banking_system_impl import BankingSystemImpl

class TestBankingSystemImpl(unittest.TestCase):

    def setUp(self):
        self.banking_system = BankingSystemImpl()

    def test_create_account(self):
        self.assertTrue(self.banking_system.create_account(1, "account1"))
        self.assertFalse(self.banking_system.create_account(2, "account1"))

    def test_deposit(self):
        self.banking_system.create_account(1, "account1")
        self.assertEqual(self.banking_system.deposit(2, "account1", 1000), 1000)
        self.assertEqual(self.banking_system.deposit(3, "account2", 1000), None)

    def test_transfer(self):
        self.banking_system.create_account(1, "account1")
        self.banking_system.create_account(2, "account2")
        self.banking_system.deposit(3, "account1", 1000)
        self.assertEqual(self.banking_system.transfer(4, "account1", "account2", 500), 500)
        self.assertEqual(self.banking_system.transfer(5, "account1", "account2", 600), None)

    def test_pay(self):
        self.banking_system.create_account(1, "account1")
        self.banking_system.deposit(2, "account1", 1000)
        payment_id = self.banking_system.pay(3, "account1", 500)
        self.assertEqual(self.banking_system.get_payment_status(4, "account1", payment_id), "IN_PROGRESS")

    def test_top_spenders(self):
        self.banking_system.create_account(1, "account1")
        self.banking_system.create_account(2, "account2")
        self.banking_system.deposit(3, "account1", 1000)
        self.banking_system.deposit(4, "account2", 2000)
        self.banking_system.pay(5, "account1", 500)
        self.banking_system.pay(6, "account2", 1000)
        self.assertEqual(self.banking_system.top_spenders(7, 2), ["account2(1000)", "account1(500)"])

    def test_merge_accounts(self):
        self.banking_system.create_account(1, "account1")
        self.banking_system.create_account(2, "account2")
        self.banking_system.deposit(3, "account1", 1000)
        self.banking_system.deposit(4, "account2", 500)
        self.banking_system.merge_accounts(5, "account1", "account2")
        self.assertEqual(self.banking_system.get_balance(6, "account1", 6), 1500)
        self.assertIsNone(self.banking_system.get_balance(6, "account2", 6))

if __name__ == '__main__':
    unittest.main()
