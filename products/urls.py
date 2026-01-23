from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('products',views.ProductViewSet,basename='product')

urlpatterns=[
    path('',include(router.urls)),
    path("<int:product_id>/reviews/",views.ReviewListCreateAPIView.as_view(),name="product-reviews"),
    path("reviews/<int:pk>/",views.ReviewDetailAPIView.as_view(),name="review-detail"),
    path("<int:product_id>/can-review/",views.CanReviewAPIView.as_view()),
    path('banner/',views.ProductBannerAPIView.as_view()),
    path('latest-banner/',views.LatestProductsBannerAPIView.as_view()),


]