from rest_framework import serializers   
from .model import Product,Category  

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category 
		fields = ['id','name','parent']

class ProductSerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only = True)
	category_id = serializers.PrimaryKeyRelatedField(
		queryset = Category.objects.all(),
		source = "category",
		write_only = True
		)
class Meta:
	model = Product 
	fields = ['id','seller','name','description','price','quantity','category','category_id','image','status','created_at','updated_at']
	read_only_fields =['seller','created_at','updated_at']