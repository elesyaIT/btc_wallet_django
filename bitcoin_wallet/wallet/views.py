from rest_framework import generics
from .serializers import TransactionSerializer
from rest_framework.generics import RetrieveAPIView
from .models import Transaction
from .serializers import BalanceSerializer
from decimal import Decimal, DecimalException
from rest_framework.response import Response
from rest_framework import status
import requests

def get_exchange_rate():
    try:
        response = requests.get("http://api-cryptopia.adca.sh/v1/prices/ticker")
        data = response.json()
        bitcoin_to_eur_rate = None
        for item in data['data']:
            if item['symbol'] == 'BTC/EUR':
                bitcoin_to_eur_rate = float(item['value'])
                break
        return bitcoin_to_eur_rate
    except Exception as e:
        print("Error fetching exchange rate:", e)
        return None

class WalletBalance(RetrieveAPIView):
    serializer_class = BalanceSerializer

    def get_object(self):
        unspent_transactions = Transaction.objects.filter(spent=False)
        btc_balance = sum(transaction.amount for transaction in unspent_transactions)
        bitcoin_to_eur_rate = get_exchange_rate()
        if bitcoin_to_eur_rate is not None:
            bitcoin_to_eur_rate = Decimal(str(bitcoin_to_eur_rate))
            eur_balance = btc_balance * bitcoin_to_eur_rate
            return {'btc_balance': btc_balance, 'eur_balance': eur_balance}
        else:
            return {'error': 'Failed to fetch exchange rate'}


class WalletTransactoin(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class WalletTransactionUpdate(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def update(self, request, *args, **kwargs):
        unspent_transactions = Transaction.objects.filter(spent=False)
        transfer_amount_str = request.data.get('amount')
        print(transfer_amount_str)

        try:
            transfer_amount = Decimal(transfer_amount_str)
        except DecimalException:
            return Response({'error': 'Invalid transfer amount.'}, status=status.HTTP_400_BAD_REQUEST)

        bitcoin_to_eur_rate = get_exchange_rate()
        if bitcoin_to_eur_rate is None:
            return Response({'error': 'Failed to fetch exchange rate.'}, status=status.HTTP_400_BAD_REQUEST)

        bitcoin_to_eur_rate = Decimal(str(bitcoin_to_eur_rate))

        bitcoin_amount = transfer_amount / bitcoin_to_eur_rate

        if bitcoin_amount <= 0:
            return Response({'error': 'Invalid transfer amount.'}, status=status.HTTP_400_BAD_REQUEST)

        total_unspent_amount = sum(transaction.amount for transaction in unspent_transactions)

        if total_unspent_amount < bitcoin_amount:
            return Response({'error': 'Not enough unspent balance for the transfer.'},
                            status=status.HTTP_400_BAD_REQUEST)

        for transaction in unspent_transactions:
            if bitcoin_amount > 0 and bitcoin_amount <= transaction.amount:
                leftover_amount = transaction.amount - bitcoin_amount
                if leftover_amount > 0:
                    Transaction.objects.create(amount=leftover_amount, spent=False)
                transaction.spent = True
                transaction.amount = bitcoin_amount
                transaction.save()
                break
            elif bitcoin_amount > 0:
                bitcoin_amount -= transaction.amount
                transaction.amount = 0
                transaction.spent = True
                transaction.save()

        unspent_transactions = Transaction.objects.filter(spent=False)

        serializer = self.get_serializer(unspent_transactions, many=True)
        return Response(serializer.data)
