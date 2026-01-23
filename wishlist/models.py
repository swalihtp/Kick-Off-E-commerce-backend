from django.db import models
from accounts.models import User
from products.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product_wishlist'
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.product}"

