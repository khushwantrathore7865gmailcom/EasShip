import datetime

from django.db import models
from User.models import User_custom
from django.core.validators import RegexValidator


# Create your models here.
class customer(models.Model):
    user = models.ForeignKey(User_custom, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"


#

class Customer_profile(models.Model):
    cust = models.ForeignKey(customer, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 91XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    email = models.EmailField(max_length=25, blank=True, )
    company_type = models.CharField(max_length=250, blank=True, )
    company_name = models.CharField(max_length=250, blank=True, )
    company_logo = models.ImageField(blank=True, )


class Customer_address(models.Model):
    cust = models.ForeignKey(customer, on_delete=models.CASCADE)
    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )
    state = models.CharField(
        "State",
        max_length=1024,
    )

    country = models.CharField(
        "Country",
        max_length=1024,
    )

    class Meta:
        verbose_name = "Customer Company Address"
        verbose_name_plural = "Customer Company Addresses"


class shipJob(models.Model):
    cust = models.ForeignKey(customer, on_delete=models.CASCADE)
    ship_title = models.CharField(max_length=1024, null=True)
    job_description = models.CharField(blank=True, max_length=1024)
    picking_Address = models.CharField(max_length=1024)
    droping_Address = models.CharField(max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    bid_selected = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


class ProdDesc(models.Model):
    shipment = models.ForeignKey(shipJob, on_delete=models.CASCADE, null=True)
    prod_box = models.IntegerField()
    prod_in_box = models.IntegerField()
    Weight_box = models.CharField(max_length=1024)
    length = models.CharField(max_length=1024)
    width = models.CharField(max_length=1024)
    height = models.CharField(max_length=1024)


class Expired_ShipJob(models.Model):
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)


class Shipment_Related_Question(models.Model):
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer_size = models.IntegerField(default=10)
