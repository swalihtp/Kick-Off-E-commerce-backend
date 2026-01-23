from django.urls import path
from . import views


urlpatterns=[
    path('users/',views.UserAPIView.as_view()),
    path('listbycategory/',views.ProductListView.as_view(), name='product-list'),
    path('categories/',views.CategoryView.as_view()),
    path('orders/',views.AdminOrderListView.as_view(),name='admin-orders'),
    path('markdelivered/',views.MarkDeliveredView.as_view(),name='mark-delivered'),
    path('admins/',views.ListAdminAPIView.as_view()),
    path('userdetails/<int:id>/',views.UserDetailsAPIView.as_view()),
    path('users/<int:id>/orders/',views.UserOrdersAPIView.as_view()),
    path('search/',views.AdminSearchAPIView.as_view())
]