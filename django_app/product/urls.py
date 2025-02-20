from django.urls import path 
from .views import ProductListCreateView,ProductDetailView,CategoryListView

urlpatterns = [
   path('Product/',ProductListCreateView.as_view(),name="Product-list-create"),
   path('Product/<int:pk>/',ProductDetailView.as_view(), name="Product-detail"),
   path('categories/',CategoryListView.as_view(),name="category-list"),
]
