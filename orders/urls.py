from django.urls import path
from . import views

urlpatterns=[
    path('',views.PlaceOrderAPIView.as_view()),
    path('view/',views.ViewOrdersAPIView.as_view()),
    path("<int:order_id>/cancel/", views.CancelOrderAPIView.as_view()),
]