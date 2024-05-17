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

    customer = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.00
    )

    def __str__(self):
        return f"Order - {self.customer} "

    def update_total_price(self):
        total_price = sum(
            item.quantity * item.drug.price_per_item for item in self.items.all()
        )
        self.total_price = total_price
        self.save()


class OrderItem(models.Model):
    ORDER_STATUS_CHOICES = (
        ("pending", "pending"),
        ("processing", "processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default="pending"
    )
    orders = models.ManyToManyField(Order, related_name="items", blank=True)

    def __str__(self):
        return f"{self.drug}"

    @property
    def getCustomer(self):
        orders = self.orders.all()
        customer = set(order.customer for order in orders)
        return customer

    def calculate_total_price(self):
        # Convert quantity and price_per_item to numeric types if they are strings
        try:
            quantity = int(self.quantity)
            price_per_item = Decimal(self.price_per_item)
        except (TypeError, ValueError):
            # Handle conversion errors
            return Decimal(0.00)

        # Calculate total price and round it to 2 decimal places
        total_price = round(quantity * price_per_item, 2)
        return total_price

    def save(self, *args, **kwargs):
        # Calculate total price before saving
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
        # update stock quantity for associated drugs
        # for order in self.orders.all():
        #     for drug in order.items.all():
        #         drug.updateStock(self.quantity)
        # Update total price for associated orders
        for order in self.orders.all():
            order.update_total_price()
