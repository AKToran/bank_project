from typing import Any
from django import forms
from .models import Transactions, TransferMoney
from accounts.models import UserBankAccount
from core.models import Bank

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam 
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self): #* amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') 
        #* user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
        
        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000
        amount = self.cleaned_data.get('amount')
        
        if Bank.objects.filter(is_bankrupt= True).exists():
            raise forms.ValidationError(
                f'Bank is bankrupt and no money to withdraw!'
            )
        
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'Minimum Withdraw Amount: {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount


class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount 


class TransferMoneyForm(forms.ModelForm):
    class Meta:
        model = TransferMoney
        fields = ['receiver', 'amount']

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender')
        super().__init__(*args, **kwargs)


    def save(self, commit = True):
        self.instance.sender = self.sender
        return super().save()
    
    def clean_receiver(self):
        receiver = self.cleaned_data.get('receiver')
        
        try:
            UserBankAccount.objects.get(account_no=receiver)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError("Account not found!")
        return receiver

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        balance = self.sender.balance

        if amount < 0 or amount > balance:
            raise forms.ValidationError('Enter a valid amount!')
        return amount
        