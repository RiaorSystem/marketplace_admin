from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Order, OrderItem
from products.models import Product
from .serializers import CartSerializer, OrderSerializer
from django.db import transaction
from users.permissions import IsSeller

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        product_id  = request.data.get("product")

        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            return Response({"message": "Item removed form cart"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_amount =  sum(item.subtotal() for item in cart_items)
        order = Order.objects.create(user=request.user, total_amount=total_amount)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateOrderStatusView(APIView):
    permission_classes = [IsSeller, IsAuthenticated]

    def put(self, request, order_id):
        new_status = request.data.get("status")
        
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        order_items = OrderItem.objects.filter(order=order, product__seller=request.user)
        if not order_items.exists():
            return Response({"error": " You don't have permission to upddate this order"}, status=status.HTTP_403_FORBIDDEN)
        
        order.status = new_status
        order.save()

        return Response({"message": f"Order stsus updated to {new_status}"}, status=status.HTTP_200_OK)