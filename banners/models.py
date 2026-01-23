from django.db import models

class BannerSlot(models.Model):
    key = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.key
class Banner(models.Model):
    TEMPLATE_CHOICES = [
        ('hero_left', 'Hero Text Left'),
        ('hero_center', 'Hero Text Center'),
        ('campaign_card', 'Campaign Card'),
        ('category_tile', 'Category Tile'),
        ('strip', 'Offer Strip'),
    ]

    template_type = models.CharField(
        max_length=30,
        choices=TEMPLATE_CHOICES,
        null=True,
        blank=True
    )
    
    slot = models.ForeignKey(BannerSlot, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)

    image_desktop = models.ImageField(upload_to="banners/desktop/")
    image_mobile = models.ImageField(upload_to="banners/mobile/", null=True, blank=True)

    link_type = models.CharField(
        max_length=20,
        choices=[
            ('product', 'Product'),
            ('category', 'Category'),
            ('collection', 'Collection'),
            ('external', 'External'),
        ]
    )
    link_value = models.CharField(max_length=255)

    priority = models.IntegerField(default=0)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} Banner "

