from django.db import models
from accounts.models import User
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
        
