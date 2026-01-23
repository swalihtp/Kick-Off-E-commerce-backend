from django.urls import path
from .views import DashboardAnalyticsView

urlpatterns = [
    path("analytics/", DashboardAnalyticsView.as_view()),
]
