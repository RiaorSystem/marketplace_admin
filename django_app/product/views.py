from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser 
from .model import Product, Category 
from .serializers import ProfileSerializer, CategorySerializer, ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self,serializers):
        serializers.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.object.all()
    serializers_class = ProductSerializer 
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
     
     return Product.objects.filter(seller=self.request.user)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    