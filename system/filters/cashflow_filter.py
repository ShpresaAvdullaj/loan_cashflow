from system.models.cashflows import CashFlow
import django_filters


class CashFlowFilter(django_filters.FilterSet):
    class Meta:
        model = CashFlow
        fields = {'loan_identifier': ['exact'],
                  'amount': ['exact', 'lte', 'gte'],
                  'type': ['exact', 'contains'],
                  'reference_date': ['exact', 'lte', 'gte']}
