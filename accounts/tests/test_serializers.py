from django.test import TestCase
from accounts.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from accounts.serializers import LoginSerializer


User = get_user_model()

class RegisterSerializerTest(TestCase):

    def test_valid_data_creates_user(self):
        data = {
            "email": "new@test.com",
            "password": "strongpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, data["email"])

    def test_duplicate_email_fails(self):
        User.objects.create_user(
            email="dup@test.com",
            password="pass12345"
        )

        data = {
            "email": "dup@test.com",
            "password": "strongpass123"
        }

        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

class LoginSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="login@test.com",
            password="loginpass123"
        )

    def test_login_with_valid_credentials(self):
        data = {
            "email": "login@test.com",
            "password": "loginpass123"
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_login_with_invalid_credentials(self):
        data = {
            "email": "login@test.com",
            "password": "wrongpass"
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
