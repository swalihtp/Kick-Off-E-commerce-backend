from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        user=User.objects.create_user(
            email='test@gmail.com',
            password='test@123'
        )
        self.assertEqual(user.email,'test@gmail.com')
        self.assertTrue(user.check_password('test@123'))
        