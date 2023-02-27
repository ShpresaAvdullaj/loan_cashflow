from rest_framework import serializers
from system.models.loans import Loan


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = "__all__"
