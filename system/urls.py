from django.urls import path
from system.views.views import LoanViewSet, CashFlowList, LoanList

urlpatterns = [
    path("upload/", LoanViewSet.as_view({"post": "upload_files"}), name="upload-files"),
    path("delete/", LoanViewSet.as_view({"delete": "delete_db"}), name="delete-data"),
    path("statistics/", LoanViewSet.as_view({"get": "statistics_of_investments"}), name="statistics_of_investments"),
    path("loans/<int:loan_pk>/create_repayment/", LoanViewSet.as_view({"post": "create_repayment"}), name="create_repayment"),
    path("cashflows", CashFlowList.as_view(), name="all_cashflows"),
    path("loans", LoanList.as_view(), name="all_loans")
]
