from rest_framework import serializers
from system.models.cashflows import CashFlow


class RepaymentCashFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashFlow
        fields = ("reference_date", "amount", )
