from system.models.cashflows import CashFlow
from django_filters import rest_framework as filters


class CashFlowFilter(filters.FilterSet):
    loan_identifier = filters.CharFilter(field_name="loan_identifier", lookup_expr='exact')
    amount__lte = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    amount__gte = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    amount = filters.NumberFilter(field_name="amount", lookup_expr='exact')

    class Meta:
        model = CashFlow
        fields = ['loan_identifier', 'amount__lte', "amount__gte", "amount"]