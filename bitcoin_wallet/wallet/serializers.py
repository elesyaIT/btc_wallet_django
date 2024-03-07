from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    Serializes the Transaction model to and from JSON format.
    Attributes:
        model (Transaction): The model class to serialize/deserialize.
        fields (list): The fields to include in the serialized data.
    """

    class Meta:
        model = Transaction
        fields = "__all__"

class BalanceSerializer(serializers.Serializer):
    """
    Serializes the balance data to and from JSON format.
    Attributes:
        btc_balance (FloatField): The balance in bitcoins.
        eur_balance (FloatField): The balance in euros.
    """

    btc_balance = serializers.FloatField()
    eur_balance = serializers.FloatField()
