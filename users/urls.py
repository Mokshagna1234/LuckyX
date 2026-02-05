from django.urls import path
from .views import account_page,account_details

urlpatterns = [
    path('', account_page),                 
    path('details/', account_details),
]
