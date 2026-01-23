from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.RegisterApiView.as_view()),
    path('verify-email/<uidb64>/<token>/',views.VerifyEmailAPIView.as_view()),
    path('login/',views.LoginApiView.as_view()),
    path('logout/',views.LogoutApiView.as_view()),
    path("google/", views.GoogleAuthView.as_view()),
    path('profile/',views.ProfileView.as_view()),
    path("forgot-password/",views.ForgotPasswordView.as_view()),
    path("reset-password/", views.ResetPasswordView.as_view()),
    path("register-admin/",views.RegisterAdminAPIView.as_view()),
]