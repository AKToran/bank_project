from django.db import models
from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE

class Transactions(models.Model):
    # * one account per transaction. many transactions on a single account
    account = models.ForeignKey(UserBankAccount, related_name="transactions", on_delete=models.CASCADE)

    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False)

    class Meta: 
        ordering = ['timestamp']

class TransferMoney(models.Model):
    sender = models.ForeignKey(UserBankAccount, related_name="money_sent", on_delete=models.DO_NOTHING)
    # receiver = models.ForeignKey(UserBankAccount, related_name="money_received", on_delete=models.DO_NOTHING)
    receiver = models.DecimalField(max_digits=6, decimal_places=0)
    amount = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return f"from {self.sender} to {self.receiver}"
