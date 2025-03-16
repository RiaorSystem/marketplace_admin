from django.db import models
from users.models import CustomUser

class Advertisement(models.Model):
    """Sellers create advertisement opportunities"""
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ads_created")
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.seller.username}"

class AdvertisementApplication(models.Model):
    """Buyers apply to run advertisements"""
    advertiser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ads_applied")
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="applications")  # ✅ This must exist
    engagement_stats = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Automatically assign buyer to escrow when approved"""
        super().save(*args, **kwargs)
        if self.approved:
            escrow = Escrow.objects.get(advertisement=self.advertisement)
            escrow.buyer = self.advertiser
            escrow.save()

    def __str__(self):
        return f"Ad {self.advertisement.title} - {self.advertiser.username}"

class Escrow(models.Model):
    """Escrow system to hold advertisement funds securely"""
    STATUS_CHOICES = [
        ("holding", "Holding"),
        ("released", "Released"),
        ("cancelled", "Cancelled"),
    ]

    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, related_name="escrow")
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="escrows_created")
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="escrows_received", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="holding")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Escrow for {self.advertisement.title} - {self.status}"

    def release_funds(self):
        """Release funds to the buyer"""
        if self.status == "holding" and self.buyer:
            wallet, created = EscrowWallet.objects.get_or_create(owner=self.buyer)
            if wallet.release_funds(self.amount):
                self.status = "released"
                self.save()
                return True
        return False

class EscrowWallet(models.Model):
    """Escrow wallet to hold funds before release"""
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="escrow_wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def deposit(self, amount):
        """Deposit funds into escrow"""
        if amount > 0:
            self.balance += amount
            self.save()

    def release_funds(self, amount):
        """Release funds to the advertiser"""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False
