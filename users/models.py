from django.db import models
from django.contrib.auth.models import User
import string
import random

# Create your models here.
def generate_user_public_id(username):
    prefix = username[:3].upper()
    digits = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}{digits}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    public_id = models.CharField(max_length=6, unique=True)

    def save(self, *args, **kwargs):
        if not self.public_id:
            while True:
                new_id = generate_user_public_id(self.user.username)
                if not UserProfile.objects.filter(public_id=new_id).exists():
                    self.public_id = new_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.public_id