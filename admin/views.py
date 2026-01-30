from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from . serializers import UsersSerializer
from rest_framework.response import Response
from products.models import Product,Category
from products.serializers import ProductSerializer,CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework.permissions import IsAdminUser
from django.db.models import Q


class UserAPIView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        users=User.objects.filter(is_superuser=False)
        serializer=UsersSerializer(users,many=True,context={'request':request})
        return Response(serializer.data)
    
    def patch(self, request):
        user_id = request.data.get('id')
        is_active = request.data.get('status')

        if user_id is None or is_active is None:
            return Response(
                {'error': 'id and status are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)

        user.is_active = is_active
        user.save()

        return Response(
            {
                'message': 'User status updated',
                'user_id': user.id,
                'is_active': user.is_active
            },
            status=status.HTTP_200_OK
        )
    
class ProductListView(ListAPIView):
    permission_classes=[IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__name']

class CategoryView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data)

class AdminOrderListView(ListAPIView):
    parser_classes=[IsAdminUser]
    queryset = Order.objects.all().prefetch_related(
        'items__product'
    ).select_related('user')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    
class MarkDeliveredView(APIView):
    permission_classes=[IsAdminUser]
    def patch(self,request):
        order=Order.objects.get(id=request.data['order_id'])
        order.order_status='delivered'
        order.save()
        return Response({'message':'order is delivered '})
    
class ListAdminAPIView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        admins=User.objects.filter(is_staff=True)
        serializer=UsersSerializer(admins,many=True,context={'request':request})
        return Response(serializer.data)
    
class UserDetailsAPIView(APIView):
    def get(self,request,id):
        user=User.objects.get(id=id)
        serializer=UsersSerializer(user,context={'request':request})
        return Response(serializer.data)
    
    def delete(self,request,id):
        user=User.objects.get(id=id)
        user.delete()
        return Response({'message':'user deleted successfully'})
    
class UserOrdersAPIView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Order.objects.filter(
            user_id=user_id
        ).select_related('user').prefetch_related('items__product')

class AdminSearchAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response({
                "users": [],
                "products": [],
                "orders": []
            })

        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )[:5]

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )[:5]

        return Response({
            "users": [
                {
                    "id": u.id,
                    "email": u.email,
                    "name": f"{u.first_name} {u.last_name}",
                } for u in users
            ],
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                } for p in products
            ]
        })

        