from django.contrib import admin

from .models import Transactions
from .views import send_transaction_email
# admin.site.register(Transactions)

# *this decorator allows us to modify what to show in the admin interface
@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approve']
    
    def save_model(self, request, obj, form, change):
        if obj.loan_approve == True:
            obj.account.balance += obj.amount
            obj.balance_after_transaction = obj.account.balance
            obj.account.save()
            send_transaction_email(obj.account.user, obj.amount, "Loan Approved",'transactions/loan_approve.html')
        super().save_model(request, obj, form, change)
