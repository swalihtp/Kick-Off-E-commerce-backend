from django.urls import path
from . import views

urlpatterns=[
    path('homepage-banners/',views.HomepageBannerAPIView.as_view())
]