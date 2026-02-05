from django.urls import path
from .views import wallet_page, wallet_balance

urlpatterns = [
    path('', wallet_page, name='wallet'),
    path('balance/', wallet_balance, name='wallet_balance'),
]
