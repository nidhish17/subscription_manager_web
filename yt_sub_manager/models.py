from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)


class Category(models.Model):
    user_profile = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "categories")
    name = models.CharField(max_length= 255)

    def __str__(self):
        return self.name


class Channel(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= "channel")
    channel_name = models.CharField(max_length= 500)
    channel_url = models.URLField()
    pic_url = models.URLField()
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "channel_user")
