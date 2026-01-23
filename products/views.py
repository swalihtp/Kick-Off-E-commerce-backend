from .models import Product,Review
from .serializers import ProductSerializer,ReviewSerializer
from .permisssions import IsAdminOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from orders.models import OrderItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=[IsAdminOrReadOnly]

class ReviewListCreateAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.kwargs.get('product_id')

       
        has_purchased = OrderItem.objects.filter(
            order__user=user,
            order__order_status="delivered",
            product_id=product_id
        ).exists()

        if not has_purchased:
            raise PermissionDenied(
                "You can review only products you have purchased."
            )

        if Review.objects.filter(user=user, product_id=product_id).exists():
            raise ValidationError(
                "You have already reviewed this product."
            )

        serializer.save(
            user=user,
            product_id=product_id
        )

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionDenied("You can edit only your review")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("You can delete only your review")
        instance.delete()
        
class CanReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        can_review = OrderItem.objects.filter(
            order__user=request.user,
            order__order_status="delivered",
            product_id=product_id
        ).exists()

        return Response({"can_review": can_review})

class ProductBannerAPIView(APIView):
    def get(self, request):
        product = (
            Product.objects
            .filter(stock__lte=5)
            .order_by('stock')
            .first()
        )

        if not product:
            return Response({"message": "No banner product available"})

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
class LatestProductsBannerAPIView(APIView):
    def get(self, request):
        products = (
            Product.objects
            .order_by('-created_at')[:6]
        )

        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )

        return Response({
            "headline": "Fresh Arrivals",
            "tagline": "Discover the latest products added just for you",
            "products": serializer.data
        })