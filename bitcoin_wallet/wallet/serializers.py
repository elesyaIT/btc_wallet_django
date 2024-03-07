from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

class BalanceSerializer(serializers.Serializer):
    btc_balance = serializers.FloatField()
    eur_balance = serializers.FloatField()

