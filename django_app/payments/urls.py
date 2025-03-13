from django.urls import path
from .views import MpesaPaymentView, mpesa_webhook

urlpatterns = [
    path('mpesa/', MpesaPaymentView.as_view(), name='mpesa'),
    path('mpesa/webhook/' , mpesa_webhook, name='mpesa_webhook'),
]