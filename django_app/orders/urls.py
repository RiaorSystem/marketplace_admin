from django.urls import path
from .views import CartView, CheckoutView, OrderHistoryView, UpdateOrderStatusView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderHistoryView.as_view(), name='order_history'),
    path('orders/<int:order_id>/update/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]
