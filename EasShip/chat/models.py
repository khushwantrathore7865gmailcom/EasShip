from django.db import models
from User.models import User_custom
from datetime import datetime


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=1000000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User_custom, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=1000,null=True)