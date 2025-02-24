from rest_framework import serializers   
from .models import Product,Category  

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category 
		fields = ['id','name','parent']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for managing products"""
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    seller = serializers.ReadOnlyField(source='seller.email')  # Prevent manual seller assignment

    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'description', 'price', 'stock', 'image', 'category', 'category_id', 'rating']
        read_only_fields = ['id', 'seller', 'rating']
