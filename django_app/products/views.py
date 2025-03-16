from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from users.permissions import IsSeller

class SellerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        products = Product.objects.filter(seller=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductListView(APIView):
    def get(self, request):
        category = request.query_params.get("category",  None)
        min_price = request.query_params.get("min_price", None)
        max_price = request.query_params.get("max_price", None)
        min_rating = request.query_params.get("min_rating", None)

        products = Product.objects.all()

        if category:
            products = products.filter(category__name__icontains=category)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if min_rating:
            products = products.filter(rating__gte=min_rating)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductCreateView(APIView):
    """Create a new product (Seller Only)"""
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):
        """Assign logged-in user as seller and create product"""
        data = request.data.copy()
        data['seller'] = request.user.id  

        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save(seller=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get_object(self, product_id, user):
        try:
            return Product.objects.get(id=product_id, seller=user)
        except Product.DoesNotExist:
            return None
        
    def get(self, request, product_id):
        product = self.get_object(product_id, request.user)
        if not product:
            return Response({"error": "Product not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, product_id):
        product = self.get_object(product_id, request.user)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, product_id):
        product = self.get_object(product_id, request.user)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({"message": "Product deleted successfully"},status=status.HTTP_204_NO_CONTENT)