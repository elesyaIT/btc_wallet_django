from django.contrib import admin
from django.urls import path

from wallet.views import WalletTransactoin, WalletTransactionUpdate, WalletBalance

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/walletlist/add_transaction/', WalletTransactoin.as_view()),
    path('api/v1/walletlist/spent_eur/', WalletTransactionUpdate.as_view()),
    path('balance/', WalletBalance.as_view()),
]
