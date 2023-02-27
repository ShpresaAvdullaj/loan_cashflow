from django.db import models
from system.models.cashflows import CashFlow
from django.db.models import Sum
from pyxirr import xirr


class Loan(models.Model):
    identifier = models.CharField(max_length=25, unique=True)
    issue_date = models.DateField()
    total_amount = models.FloatField()
    rating = models.IntegerField()
    maturity_date = models.DateField()
    total_expected_interest_amount = models.FloatField()

    invested_amount = models.FloatField(default=0)
    investment_date = models.DateField(null=True)
    expected_interest_amount = models.FloatField(default=0)
    expected_irr = models.FloatField(default=0)
    is_closed = models.BooleanField(default=False)
    realized_irr = models.FloatField(default=0)

    def get_calculated_fields(self):
        funding = CashFlow.objects.filter(loan_identifier=self.identifier, type="Funding")
        self.invested_amount = abs(funding.aggregate(Sum("amount"))["amount__sum"])
        self.investment_date = funding.first().reference_date
        self.expected_interest_amount = float(self.total_expected_interest_amount) * float(self.invested_amount) / float(self.total_amount)

    def expected_irr_calculation(self):
        funding = CashFlow.objects.filter(loan_identifier=self.identifier, type="Funding")
        # The funding
        date_funding = [c.reference_date for c in funding]
        amount_funding = [c.amount for c in funding]
        # The expected repayment
        date_funding.append(self.maturity_date)
        amount_funding.append(float(self.invested_amount) + float(self.expected_interest_amount))
        expected_irr = xirr(zip(date_funding, amount_funding))
        self.expected_irr = expected_irr

    def is_closed_loan(self):
        repayment = CashFlow.objects.filter(loan_identifier=self.identifier, type="Repayment")
        if repayment.exists():
            expected_amount = float(self.invested_amount) + float(self.expected_interest_amount)
            total_repaid_amount = repayment.aggregate(Sum("amount"))["amount__sum"]
            if total_repaid_amount >= expected_amount:
                self.is_closed = True

    def realized_irr_calculation(self):
        funding = CashFlow.objects.filter(loan_identifier=self.identifier, type="Funding")
        repayment = CashFlow.objects.filter(loan_identifier=self.identifier, type="Repayment")
        if self.is_closed:
            # The funding
            date_funding = [c.reference_date for c in funding]
            amount_funding = [c.amount for c in funding]
            # The repayment
            date_repayment = [c.reference_date for c in repayment]
            amount_repayment = [c.amount for c in repayment]
            dates = date_funding + date_repayment
            amounts = amount_funding + amount_repayment
            realized_irr = xirr(zip(dates, amounts))
            self.realized_irr = realized_irr
