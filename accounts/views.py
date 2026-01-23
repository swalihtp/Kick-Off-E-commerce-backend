from rest_framework.views import APIView
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from admin.serializers import UsersSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAdminUser
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404


class RegisterApiView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            #  Generate token
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            #  Verification link
            verification_link = (
                f"http://localhost:5173/verify-email/"
                f"{uid}/{token}/"
            )

            #  Send email
            send_mail(
                subject="Verify your email address",
                message=(
                    f"Hello {user.first_name},\n\n"
                    f"Thank you for registering.\n\n"
                    f"Please verify your email by clicking the link below:\n\n"
                    f"{verification_link}\n\n"
                    f"If you did not create this account, please ignore this email.\n\n"
                    f"Regards,\nTeam"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response(
                {"message": "Registration successful. Please check your email to verify your account."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPIView(APIView):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except Exception:
            return Response(
                {"error": "Invalid verification link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"message": "Email verified successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Verification link expired or invalid"},
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginApiView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            refresh=RefreshToken.for_user(user)
            return Response({'refresh':str(refresh),'access':str(refresh.access_token),"role":user.role},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LogoutApiView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        refresh_token=request.data.get('refresh')
        token=RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message":"Logged out successfully"})
    
class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get("token")

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]
            name = idinfo.get("name")

            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": email, "first_name": name}
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        except ValueError:
            return Response({"error": "Invalid token"}, status=400)

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=UsersSerializer(request.user,context={'request':request})
        return Response(serializer.data)
    
    def patch(self,request):
        serializer=UsersSerializer(request.user,data=request.data,partial=True,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"

        send_mail(
            "Password Reset",
            f"Click the link to reset password: {reset_link}",
            "noreply@example.com",
            [email],
        )

        return Response({"message": "Password reset link sent check your email"})

class ResetPasswordView(APIView):
    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except:
            return Response({"error": "Invalid UID"}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.password = make_password(password)
        user.save()

        return Response({"message": "Password reset successful"})

class RegisterAdminAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only superusers can create admins"},
                status=403
            )

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            password = request.data.get('password')
            user = serializer.save(is_staff=True)

            # Sending  email
            send_mail(
                subject='Your Admin Account Has Been Created',
                message=(
                    f"Hello {user.first_name},\n\n"
                    f"Your admin account has been successfully created.\n\n"
                    f"Login Email: {user.email}\n"
                    f"Password: {password}\n\n"
                    f"Please change your password after logging in.\n\n"
                    f"Thankyou,\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "Admin created and email sent successfully"},
                status=201
            )

        return Response(serializer.errors, status=400)
