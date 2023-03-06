from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from system.serializers.repayment_serializer import RepaymentCashFlowSerializer
from system.serializers.cashflow_serializer import CashFlowSerializer
from system.serializers.loan_serializer import LoanSerializer
from rest_framework.decorators import action
from system.models.loans import Loan
from system.models.cashflows import CashFlow
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import Sum, F
from system.filters.loan_filter import LoanFilter
from system.filters.cashflow_filter import CashFlowFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from system.tasks import populate_database
from django.core.files.storage import FileSystemStorage


class LoanViewSet(ViewSet):

    @action(detail=False, methods=["POST"])
    def upload_files(self, request, *args, **kwargs):
        loan_file = request.FILES.get('loan_file')
        cashflow_file = request.FILES.get('cashflow_file')
        storage = FileSystemStorage()
        storage.save(loan_file.name, loan_file)
        storage.save(cashflow_file.name, cashflow_file)
        populate_database.delay(
            path_loan=storage.path(loan_file.name), path_cashflow=storage.path(cashflow_file.name))
        return Response("You have uploaded your files")

    @action(detail=False, methods=["POST"], serializer_class=RepaymentCashFlowSerializer)
    def create_repayment(self, request, loan_pk):
        loan = Loan.objects.get(id=loan_pk)
        serializer = RepaymentCashFlowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(loan_identifier=loan.identifier, type="Repayment")
        loan.calculated_fields()
        loan.expected_irr_calculation()
        loan.is_closed_loan()
        loan.realized_irr_calculation()
        loan.save()
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    # @method_decorator(cache_page(60), name="statistics")
    def statistics_of_investments(self, request):
        number_of_loans = Loan.objects.all().count()
        total_invested_amount = Loan.objects.all().aggregate(Sum("invested_amount"))["invested_amount__sum"]
        current_invested_amount = Loan.objects.filter(is_closed=False).aggregate(Sum("invested_amount"))["invested_amount__sum"]
        total_repaid_amount = CashFlow.objects.filter(type="Repayment").aggregate(Sum("amount"))["amount__sum"]
        average_realized_irr = Loan.objects.filter(is_closed=True).aggregate(
            w_avg=Sum(F("invested_amount") * F("realized_irr")) / Sum(F("invested_amount")))["w_avg"]

        statistics = {"number_of_loans": number_of_loans, "total_invested_amount": total_invested_amount,
                      "current_invested_amount": current_invested_amount, "total_repaid_amount": total_repaid_amount,
                      "average_realized_irr": average_realized_irr}
        cache.set("statistics", statistics)
        return Response(statistics)

    @action(detail=False, methods=["DELETE"])
    def delete_db(self, request):
        Loan.objects.all().delete()
        CashFlow.objects.all().delete()
        return Response({"error": "Yes"})


class LoanList(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LoanFilter


class CashFlowList(generics.ListAPIView):
    queryset = CashFlow.objects.all()
    serializer_class = CashFlowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashFlowFilter
