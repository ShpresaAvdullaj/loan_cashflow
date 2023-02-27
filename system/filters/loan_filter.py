from system.models.loans import Loan
import django_filters


class LoanFilter(django_filters.FilterSet):
    class Meta:
        model = Loan
        fields = {'identifier': ['exact'],
                  'invested_amount': ['exact', 'lte', 'gte'],
                  'total_amount': ['exact', 'lte', 'gte'],
                  'issue_date': ['exact', 'lte', 'gte']}
