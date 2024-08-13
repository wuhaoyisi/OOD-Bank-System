from banking_system import BankingSystem

class BankingSystemImpl(BankingSystem):
    
    milliseconds = 24*60*60*1000
    def __init__(self):
        # TODO: implement
        self.accounts = {}
        self.outgoing_transactions = {}
        self.payments = {}
        self.payment_counter = 0
        self.cashback_events = []
        self.balance_history = {}

    # TODO: implement interface methods here
    def create_account(self, timestamp, account_id):
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = 0
        self.outgoing_transactions[account_id] = 0
        self.balance_history[account_id].append((timestamp, 0))
        return True
        
    def deposit(self, timestamp, account_id, amount):
        if account_id not in self.accounts:
            return None
        self._process_cashbacks(timestamp)
        self.accounts[account_id] += amount
        self.balance_history[account_id].append((timestamp, self.accounts[account_id]))
       
        return self.accounts[account_id]
        
    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        if source_account_id == target_account_id:
            return None
        if amount > self.accounts[source_account_id]:
            return None
        self._process_cashbacks(timestamp)
        self.accounts[source_account_id] -= amount
        self.accounts[target_account_id] += amount
        self.outgoing_transactions[source_account_id] += amount
        self.balance_history[source_account_id].append((timestamp, self.accounts[source_account_id]))
        self.balance_history[target_account_id].append((timestamp, self.accounts[target_account_id]))
        
        
        return self.accounts[source_account_id]
        
    def pay(self, timestamp, account_id, amount):
        self._process_cashbacks(timestamp)
        if account_id not in self.accounts:
            return None
        if amount > self.accounts[account_id]:
            return None
        
        self.accounts[account_id] -= amount 
        self.outgoing_transactions[account_id] += amount
        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"
        self.payments[payment_id] = {
            "account_id": account_id, 
            "amount": amount, 
            "status": "IN_PROGRESS", 
            "cashback_time": timestamp + self.milliseconds
        }
        self.cashback_events.append((timestamp+self.milliseconds, account_id, amount // 50))
        self.balance_history[account_id].append((timestamp, self.accounts[account_id]))
        
        return payment_id
        
    def get_payment_status(self, timestamp, account_id, payment):
        self._process_cashbacks(timestamp)
        if account_id not in self.accounts:
            return None
        if payment not in self.payments:
            return None
        payment_info = self.payments[payment]
        if payment_info["account_id"] != account_id:
            return None
        return payment_info["status"]
        
    def top_spenders(self, timestamp, n):
        self._process_cashbacks(timestamp)
        sorted_accounts = sorted(
            self.outgoing_transactions.items(),
            key = lambda x: (-x[1], x[0]) # sort by total outgoing desc
        )
        result = [f"{account_id}({total_outgoing})" for account_id, total_outgoing in sorted_accounts[:n]]
        return result
        
    def _process_cashbacks(self, timestamp):
        events_to_process = [event for event in self.cashback_events if event[0] <= timestamp]
        for event in events_to_process:
            cashback_timestamp, account_id, cashback_amount = event
            if account_id in self.accounts:
                self.accounts[account_id] += cashback_amount
                for payment_id, payment_info in self.payments.items():
                    if payment_info["account_id"] == account_id and payment_info["cashback_time"] <= timestamp:
                        payment_info["status"] = "CASHBACK_RECEIVED"
                    self.balance_history[account_id].append((cashback_timestamp, self.accounts[account_id]))
            self.cashback_events.remove(event)
            self.cashback_events.remove(event)
            
    def merge_accounts(self, timestamp, account_id_1, account_id_2):
        if account_id_1 == account_id_2 or account_id_1 not in self.accounts or account_id_2 not in self.accounts:
            return False
        self.accounts[account_id_1] += self.accounts[account_id_2] 
        self.outgoing_transactions[account_id_1] += self.outgoing_transactions[account_id_2]
        for t, balance in self.balance_history[account_id_2]:
            self.balance_history[account_id_1].append((t, self.accounts[account_id_1]))
        for event in self.cashback_events:
            if event[1] == account_id_2:
                self.cashback_events.append((event[0], account_id_1, event[2]))
        for payment_id, payment_info in self.payments.items():
            if payment_info["account_id"] == account_id_2:
                payment_info["account_id"] = account_id_1
        del self.accounts[account_id_2]
        del self.outgoing_transactions[account_id_2]
        del self.balance_history[account_id_2]
        return True
        
    def get_balance(self, timestamp, account_id, time_at):
        if account_id not in self.accounts:
            return None
        for t, balance in reversed(self.balance_history[account_id]):
            if t <= time_at:
                return balance
        return None
        
banking_system = BankingSystemImpl()
print(banking_system.create_account(1, "account3"))
print(banking_system.create_account(2, "account2"))
print(banking_system.create_account(3, "account1"))
print(banking_system.deposit(4, "account1", 2000))
print(banking_system.deposit(5, "account2", 3000))
print(banking_system.deposit(6, "account3", 4000))
print(banking_system.top_spenders(7, 3))
print(banking_system.transfer(8, "account3", "account2", 500)) 
print(banking_system.transfer(9, "account3", "account1", 1000)) 
print(banking_system.transfer(10, "account1", "account2", 2500)) 
print(banking_system.top_spenders(11, 3))
    
