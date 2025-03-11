from django.urls import path
from .views import CartView, CheckoutView, OrderHistoryView, AdminOrderListView, AdminUpdateOrderStatusView
from .views import CartView, CheckoutView, OrderHistoryView, UpdateOrderStatusView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderHistoryView.as_view(), name='order_history'),
    path("admin/orders/", AdminOrderListView.as_view(), name="admin_orders"),
    path("admin/orders/<int:order_id>/update/", AdminUpdateOrderStatusView.as_view(), name="admin_update_order"),
    path('orders/<int:order_id>/update/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]
