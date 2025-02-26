from django.urls import path
from .views import MpesaPaymentView

urlpatterns = [
    path("mpesa/", MpesaPaymentView.as_view(), name="mpesa")
]