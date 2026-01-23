from rest_framework.views import APIView
from . models import Wishlist
from . serializers import WishlistSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from rest_framework import status

class WishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
        serializer = WishlistSerializer(wishlist_items, many=True,context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Wishlist.objects.get_or_create(
            user=request.user,
            product=serializer.validated_data['product']
        )

        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
        wishlist_serializer = WishlistSerializer(wishlist_items, many=True)

        return Response(wishlist_serializer.data, status=status.HTTP_200_OK)
    
class WishlistDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            wishlist_item = Wishlist.objects.get(user=request.user,product_id=id)
            wishlist_item.delete()
            wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
            wishlist_serializer=WishlistSerializer(wishlist_items,many=True)
            return Response(wishlist_serializer.data)
        except Wishlist.DoesNotExist:
            return Response({"detail": "Item not found in wishlist"},status=status.HTTP_404_NOT_FOUND)
