# from system.models.loans import Loan
from system.models.cashflows import CashFlow
# from django.db.models import Sum
# from pyxirr import xirr
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.cache import cache


@receiver(pre_save, sender=CashFlow)
def invalidate_cache(sender, *args, **kwargs):
    cache.delete("statistics")

# @receiver(post_save, sender=CashFlow)
# def get_calculated_fields(sender, instance, *args, **kwargs):
#     loan = Loan.objects.get(identifier=instance.loan_identifier)
#
#     # invested_amount
#     loan.invested_amount = abs(CashFlow.objects.filter(loan_identifier=loan.identifier, type="Funding").aggregate(Sum("amount"))["amount__sum"])
#
#     # investment_date
#     loan.investment_date = CashFlow.objects.filter(loan_identifier=loan.identifier, type="Funding").first().reference_date
#
#     # expected_interest_amount
#     loan.expected_interest_amount = float(loan.total_expected_interest_amount) * float(loan.invested_amount) / float(loan.total_amount)
#
#     # expected_irr
#     # The funding
#     a = [c.reference_date for c in CashFlow.objects.filter(loan_identifier=loan.identifier, type="Funding")]
#     b = [c.amount for c in CashFlow.objects.filter(loan_identifier=loan.identifier, type="Funding")]
#     # The expected repayment
#     a.append(loan.maturity_date)
#     b.append(float(loan.invested_amount) + float(loan.expected_interest_amount))
#     c = xirr(zip(a, b))
#     loan.expected_irr = c
#     loan.save()
#
#     # is_closed
#     if sender.objects.filter(loan_identifier=instance.loan_identifier, type="Repayment").exists():
#         expected_amount = float(loan.invested_amount) + float(loan.expected_interest_amount)
#         total_repaid_amount = sender.objects.filter(loan_identifier=instance.loan_identifier, type="Repayment").aggregate(Sum("amount"))["amount__sum"]
#         if total_repaid_amount >= expected_amount:
#             loan.is_closed = True
#             loan.save()
#         else:
#             loan.is_closed = False
#             loan.save()
#
#     # realized_irr
#     if loan.is_closed:
#         # The funding
#         date_funding = [c.reference_date for c in CashFlow.objects.filter(loan_identifier=loan.identifier, type="Funding")]
#         amount_funding = [c.amount for c in CashFlow.objects.filter(loan_identifier=loan.identifier, type="Funding")]
#         # The repayment
#         date_repayment = [c.reference_date for c in CashFlow.objects.filter(loan_identifier=loan.identifier, type="Repayment")]
#         amount_repayment = [c.amount for c in CashFlow.objects.filter(loan_identifier=loan.identifier, type="Repayment")]
#         dates = date_funding + date_repayment
#         amounts = amount_funding + amount_repayment
#         realized_irr = xirr(zip(dates, amounts))
#         loan.realized_irr = realized_irr
#         loan.save()
