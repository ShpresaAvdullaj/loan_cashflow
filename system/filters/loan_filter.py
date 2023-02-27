from system.models.loans import Loan
from django_filters import rest_framework as filters


class LoanFilter(filters.FilterSet):
    identifier = filters.CharFilter(field_name="identifier", lookup_expr='exact')
    invested_amount__lte = filters.NumberFilter(field_name="invested_amount", lookup_expr='lte')
    invested_amount__gte = filters.NumberFilter(field_name="invested_amount", lookup_expr='gte')
    invested_amount = filters.NumberFilter(field_name="invested_amount", lookup_expr='exact')

    class Meta:
        model = Loan
        fields = ['identifier', 'invested_amount__lte', "invested_amount__gte", "invested_amount"]
