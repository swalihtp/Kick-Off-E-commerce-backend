from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    description=models.TextField()
    stock=models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['category']),
        ]


    def __str__(self):
        return self.name
    

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

