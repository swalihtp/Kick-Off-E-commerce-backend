from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.db import transaction
from django.db.models import F
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from products.models import Product

class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.select_related().get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=400)

        #  Lock cart items + products
        cart_items = (
            cart.items
            .select_related("product")
            .select_for_update()
        )

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        #  STOCK CHECK
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {
                        "error": f"Insufficient stock for {item.product.name}. "
                                 f"Available: {item.product.stock}"
                    },
                    status=400
                )

        total_price = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        #  CREATE ORDER
        order = Order.objects.create(
            user=user,
            full_name=request.data.get("full_name"),
            email=request.data.get("email"),
            phone_number=request.data.get("phone_number"),
            address_line_1=request.data.get("address_line_1"),
            address_line_2=request.data.get("address_line_2"),
            city=request.data.get("city"),
            state=request.data.get("state"),
            country=request.data.get("country"),
            pin_code=request.data.get("pin_code"),
            payment_method=request.data.get("payment_method"),
            total_price=total_price
        )

        order_items = []

        #  DECREASE STOCK (SAFE WAY)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            # Atomic stock update
            Product.objects.filter(id=item.product.id).update(
                stock=F('stock') - item.quantity
            )   

        #  CLEAR CART
        cart_items.delete()

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id
            },
            status=201
        )

class ViewOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .prefetch_related("items__product")
            .filter(user=request.user)
        )

        
        serializer = OrderSerializer(orders, many=True,context={'request':request})
        return Response(serializer.data)

class CancelOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, order_id):
        try:
            # 🔒 Lock order row
            order = (
                Order.objects
                .select_for_update()
                .get(id=order_id, user=request.user)
            )
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.order_status in ['shipped', 'delivered', 'cancelled']:
            return Response(
                {"error": "Order cannot be cancelled at this stage"},
                status=400
            )

        # Collect product IDs
        order_items = order.items.all()
        product_ids = [item.product_id for item in order_items]

        # 🔒 LOCK PRODUCT ROWS (THIS IS THE REAL-WORLD PART)
        products = (
            Product.objects
            .select_for_update()
            .filter(id__in=product_ids)
        )

        # Restore stock
        for item in order_items:
            Product.objects.filter(id=item.product_id).update(
                stock=F('stock') + item.quantity
            )

        # Update order status
        order.order_status = 'cancelled'
        order.save(update_fields=['order_status'])

        return Response(
            {"message": "Order cancelled successfully"},
            status=200
        )
