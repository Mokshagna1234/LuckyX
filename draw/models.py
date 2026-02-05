from django.db import models
from django.contrib.auth.models import User
import string
import random

# Create your models here.
class LuckyDraw(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='OPEN')
    winner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f'Lucky Draw {self.id} - {self.status}'
    
class Participant(models.Model):
    draw=models.ForeignKey(LuckyDraw,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    joined_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.draw.id}"
    
class Ticket(models.Model):
    draw = models.ForeignKey(LuckyDraw, on_delete=models.CASCADE, related_name='tickets')
    user_profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    ticket_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            while True:
                code = ''.join(random.choices(string.digits, k=6))
                if not Ticket.objects.filter(ticket_code=code).exists():
                    self.ticket_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_code} ({self.draw.id})"