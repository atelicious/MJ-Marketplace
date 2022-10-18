from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone_number = models.CharField(max_length = 20, null = True, help_text='Enter your phone number as +63(phone number), e.g +6391-234-5678')

    def __str__(self):
        return f'{self.user.username} Profile'
