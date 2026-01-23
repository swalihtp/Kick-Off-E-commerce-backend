from django.urls import path
from .views import (
    CartApiView,
    AddToCartAPIView,
    UpdateCartItemAPIView,
    RemoveFromCartAPIView,
    # CartCountAPIView
)

urlpatterns = [
    path('', CartApiView.as_view()),
    path('add/', AddToCartAPIView.as_view()),
    path('item/<int:item_id>/', UpdateCartItemAPIView.as_view()),
    path('item/<int:item_id>/delete/', RemoveFromCartAPIView.as_view()),
    # path('cart/count/', CartCountAPIView.as_view()),
]
