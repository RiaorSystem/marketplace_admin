import requests
from django.db import models
from users.models import CustomUser
from products.models import Product

PAYMENT_METHOD_CHOICES = [
    ("mpesa", "Mpesa"),
]

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default="mpesa")
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def notify_fastapi(self):
        """Send order update to FastAPI WebSocket server"""
        url = f"http://127.0.0.1:8001/track_order/{self.id}"
        payload = {"status": self.status}  # Simplified payload
        
        try:
            response = requests.post(url, json=payload)
            print(f"📡 FastAPI Notification Response: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to notify FastAPI: {e}")

    def save(self, *args, **kwargs):
        """Notify FastAPI when order status changes"""
        if self.pk:  # Ensure order exists before updating
            old_status = Order.objects.get(pk=self.pk).status
            if old_status != self.status:
                self.notify_fastapi()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Items inside an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - Order {self.order.id}"

class Cart(models.Model):
    """Shopping cart model"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - {self.user.email}"