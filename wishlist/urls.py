from django.urls import path
from . import views

urlpatterns=[
    path('',views.WishlistAPIView.as_view()),
    path('<int:id>/delete/',views.WishlistDeleteAPIView.as_view()),
]