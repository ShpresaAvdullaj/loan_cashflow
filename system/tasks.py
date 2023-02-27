from celery import shared_task
from system.models.loans import Loan
from system.models.cashflows import CashFlow
from django.core.files.storage import FileSystemStorage
import pandas as pd
import polars as pl


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
        loan.get_calculated_fields()
        loan.expected_irr_calculation()
        loan.is_closed_loan()
        loan.realized_irr_calculation()
        loan.save()

    storage = FileSystemStorage()
    storage.delete(path_loan)
    storage.delete(path_cashflow)

    return {"Status": "Database populated"}

# Loan.create(
#     identifier=row["identifier"],
#     issue_date=row["issue_date"],
#     total_amount=row["total_amount"],
#     rating=row["rating"],
#     maturity_date=row["maturity_date"],
#     total_expected_interest_amount=row["total_expected_interest_amount"]
# )

