from rest_framework import serializers
from .models import Product,Category,Review

class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(
        source='category.name',
        read_only=True
    )
    class Meta:
        model=Product
        fields='__all__'
        read_only_fields = ('created_at', 'updated_at')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'product',
            'rating',
            'review',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'product', 'created_at']
