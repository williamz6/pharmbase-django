from django.db import models
import uuid
from datetime import timezone
from decimal import Decimal

# Create your models here.
from django.db import models
from user.models import Profile


# Create your models here.
class Drug(models.Model):
    DOSAGE_TYPE = (
        ("tablet", "Tablet"),
        ("capsule", "Capsule"),
        ("suspension", "Suspension"),
    )
    PACKAGING_SIZE = (
        ("100mg", "100mg"),
        ("200mg", "200mg"),
        ("300mg", "300mg"),
        ("400mg", "400mg"),
        ("500mg", "500mg"),
        ("30 capsules", "30 capsules"),
        ("60 capsules", "60 capsules"),
        ("90 capsules", "90 capsules"),
    )
    name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)

    packaging_size = models.CharField(
        max_length=100, choices=PACKAGING_SIZE, default="100mg"
    )
    expiration_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    stock_quantity = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    @property
    def has_expired(self):
        return self.expiration_date < timezone.now().date()

    @property
    def in_stock(self):
        return self.stock_quantity > 0


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ("pending", "pending"),
        ("processing", "processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    customer = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.00
    )
    status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default="pending"
    )
    created= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    def __str__(self):
        return f"Order {self.id} by {self.customer}"
    
    def get_drugs(self):
        return self.orderitem_set.select_related('drug')



class OrderItem(models.Model):
    
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantity} of {self.drug.name} in order {self.order.id}"

    
    # code to check if ordered quantity is more than stock quantity
  
    