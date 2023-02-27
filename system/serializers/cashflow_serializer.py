from rest_framework import serializers
from system.models.cashflows import CashFlow


class CashFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashFlow
        fields = "__all__"
