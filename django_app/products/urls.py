from django.urls import path
from .views import SellerDashboardView, ProductListView, ProductCreateView, ProductDetailView

urlpatterns = [
    path('seller/dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]
