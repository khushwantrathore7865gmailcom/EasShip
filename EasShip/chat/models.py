from django.db import models
from User.models import User_custom
from datetime import datetime
from Customer.models import customer
from PatnerCompany.models import comp_Bids, patnerComp

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    userc = models.ForeignKey(customer, on_delete=models.CASCADE,null=True)
    userp = models.ForeignKey(patnerComp,on_delete=models.CASCADE,null=True)
    bid = models.ForeignKey(comp_Bids,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"{self.name}-{self.userc}-{self.userp}"


class Message(models.Model):
    value = models.CharField(max_length=1000000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User_custom, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=1000,null=True)
    message_read = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username} send in Room : {self.room}"