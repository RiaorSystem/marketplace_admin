import requests
from django.db import models
from users.models import CustomUser
from products.models import Product

class Order(models.Model):
    """Order model"""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    PAYMENT_METHOD_CHOICES = [
        ("mpesa", "M-Pesa"),
        ("card", "Card Payment"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default="mpesa")
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"
    
class OrderItem(models.Model):
    """Items inside an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - {self.order.id}"

    def save(self, *args, **kwargs):
        """Notify FastAPI whenever order status changes"""
        if self.pk:  # Only notify if the order already exists
            old_status = Order.objects.get(pk=self.pk).status
            if old_status != self.status:
                self.notify_fastapi()
        super().save(*args, **kwargs)

    def notify_fastapi(self):
        """Send order update to FastAPI"""
        url = f"http://localhost:8001/track_order/{self.id}"
        payload = {"order_id": self.id, "status": self.status}
        try:
            requests.post(url, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"Failed to notify FastAPI: {e}")
