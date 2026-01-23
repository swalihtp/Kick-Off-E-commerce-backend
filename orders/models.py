from django.db import models

from django.db import models
from accounts.models import User
from products.models import Product

class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)

    address_line_1 = models.TextField(null=True,blank=True,default='address ')
    address_line_2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    pin_code = models.CharField(max_length=6,null=True,blank=True)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,blank=True
    )

    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
        null=True,blank=True
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    is_paid = models.BooleanField(default=False,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

