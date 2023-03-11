from celery import shared_task
from system.models.loans import Loan
from system.models.cashflows import CashFlow
from django.core.files.storage import FileSystemStorage
import pandas as pd
import polars as pl
from django.db.models import Sum, F
from django.core.mail import send_mail
from django.conf import settings


@shared_task()
def populate_database(path_loan, path_cashflow):
    cashflow_file = pd.read_csv(path_cashflow)
    for index, row in cashflow_file.iterrows():
        cashflow = CashFlow.objects.create(
            loan_identifier=row["loan_identifier"],
            reference_date=row["reference_date"],
            type=row["type"],
            amount=row["amount"])
        cashflow.save()

    loan_file = pd.read_csv(path_loan)
    for index, row in loan_file.iterrows():
        loan = Loan.objects.create(
            identifier=row["identifier"],
            issue_date=row["issue_date"],
            total_amount=row["total_amount"],
            rating=row["rating"],
            maturity_date=row["maturity_date"],
            total_expected_interest_amount=row["total_expected_interest_amount"])
        loan.calculated_fields()
        loan.expected_irr_calculation()
        loan.is_closed_loan()
        loan.realized_irr_calculation()
        loan.save()

    storage = FileSystemStorage()
    storage.delete(path_loan)
    storage.delete(path_cashflow)

    return {"Status": "Database populated"}


@shared_task()
def send_statistics():
    number_of_loans = Loan.objects.all().count()
    total_invested_amount = Loan.objects.all().aggregate(Sum("invested_amount"))["invested_amount__sum"]
    current_invested_amount = Loan.objects.filter(is_closed=False).aggregate(Sum("invested_amount"))[
        "invested_amount__sum"]
    total_repaid_amount = CashFlow.objects.filter(type="Repayment").aggregate(Sum("amount"))["amount__sum"]
    average_realized_irr = Loan.objects.filter(is_closed=True).aggregate(
        w_avg=Sum(F("invested_amount") * F("realized_irr")) / Sum(F("invested_amount")))["w_avg"]

    statistics = f"number_of_loans: {number_of_loans}, total_invested_amount: {total_invested_amount}," \
                 f"current_invested_amount: {current_invested_amount}, total_repaid_amount: {total_repaid_amount}," \
                 f"average_realized_irr: {average_realized_irr}"
    send_mail(
        subject='Email for statistics!',
        message=statistics,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['shpresa.avdullaj@fshnstudent.info'],
    )
    return "Mail sent!"
