from django.shortcuts import render

from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count

from accounts.models import User
from products.models import Product
from orders.models import Order


class DashboardAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        start_date = timezone.now() - timedelta(days=days)

        users_count = User.objects.count()
        products_count = Product.objects.count()
        orders_count = Order.objects.count()

        orders_by_day = (
            Order.objects.filter(created_at__gte=start_date)
            .extra(select={'day': "date(created_at)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        order_status = Order.objects.values('order_status').annotate(count=Count('id'))

        return Response({
            "cards": {
                "users": users_count,
                "products": products_count,
                "orders": orders_count,
            },
            "orders_by_day": orders_by_day,
            "order_status": order_status,
        })

