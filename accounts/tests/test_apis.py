from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User

class RegisterAPITest(APITestCase):

    def test_user_registration(self):
        data = {
            "email": "api@test.com",
            "password": "apipass123",
            "first_name": "API"
        }
        response = self.client.post("/api/accounts/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="api_login@test.com",
            password="loginpass123"
        )

    def test_login_success(self):
        data = {
            "email": "api_login@test.com",
            "password": "loginpass123"
        }
        response = self.client.post("/api/accounts/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        
class ProfileAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="profile@test.com",
            password="profilepass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get("/api/accounts/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
