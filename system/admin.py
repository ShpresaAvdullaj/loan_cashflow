from django.contrib import admin
from system.models.loans import Loan
from system.models.cashflows import CashFlow

admin.site.register(Loan)
admin.site.register(CashFlow)
