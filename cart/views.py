from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart,CartItem
from .serializers import CartItemSerializer,CartSerializer,AddToCartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from products.models import Product
from rest_framework import status
from django.shortcuts import get_object_or_404

class CartApiView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cart,created=Cart.objects.prefetch_related('items__product').get_or_create(user=request.user)
        serializer=CartSerializer(cart,context={'request': request})
        return Response(serializer.data)
    
class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('-------------------------------------------',request.data,'------------------------------------------------------')
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        # Get or create cart
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Get product
        product = get_object_or_404(Product, id=product_id)

        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            cart_item.quantity = quantity
            status_code = status.HTTP_201_CREATED
        else:
            cart_item.quantity += quantity
            status_code = status.HTTP_200_OK

        cart_item.save()

        # Serialize full cart with items
        cart = (
            Cart.objects
            .prefetch_related("items__product")
            .get(id=cart.id)
        )

        cart_serializer = CartSerializer(cart)

        return Response(cart_serializer.data, status=status_code)
    
class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        quantity = int(request.data.get("quantity", 0))
        if quantity < 1:
            return Response(
                {"error": "Quantity must be >= 1"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        cart = Cart.objects.prefetch_related("items__product").get(user=request.user)
        serializer = CartSerializer(cart,context={'request':request})
        return Response(serializer.data)

    
class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):

        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()
        cart = (Cart.objects.prefetch_related("items__product").get(user=request.user))
        cart_serializer=CartSerializer(cart,context={'request':request})
        return Response(cart_serializer.data)

# class CartCountAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     cart = Cart.objects.filter(user=request.user).first()

    #     if not cart:
    #         return Response({"count": 0})

    #     count = cart.items.aggregate(
    #         total=models.Sum('quantity')
    #     )['total'] or 0

    #     return Response({"count": count})

