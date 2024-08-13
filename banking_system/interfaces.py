from abc import ABC, abstractmethod

class BankingSystem(ABC):

    @abstractmethod
    def create_account(self, timestamp, account_id):
        pass

    @abstractmethod
    def deposit(self, timestamp, account_id, amount):
        pass

    @abstractmethod
    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        pass

    @abstractmethod
    def pay(self, timestamp, account_id, amount):
        pass

    @abstractmethod
    def get_payment_status(self, timestamp, account_id, payment):
        pass

    @abstractmethod
    def top_spenders(self, timestamp, n):
        pass

    @abstractmethod
    def merge_accounts(self, timestamp, account_id_1, account_id_2):
        pass

    @abstractmethod
    def get_balance(self, timestamp, account_id, time_at):
        pass
