from django.db import models
from User.models import User_custom
from django.core.validators import RegexValidator
from Customer.models import shipJob


# Create your models here.
class patnerComp(models.Model):
    user = models.ForeignKey(User_custom, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"


#

class Comp_profile(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 91XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    email = models.EmailField(max_length=25, blank=True, )
    company_type = models.CharField(max_length=250, blank=True, )
    company_name = models.CharField(max_length=250, blank=True, )
    company_logo = models.ImageField(blank=True, )


class Comp_address(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
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
        verbose_name = "Shipping Company Address"
        verbose_name_plural = "Shipping Company Addresses"


class comp_Bids(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE)
    Bid_amount = models.CharField(max_length=1024)
    complete_in = models.IntegerField()
    bid_on = models.DateTimeField(auto_now_add=True)


#
class comp_Transport(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    type_of_transport = models.CharField(max_length=1024)
    transport_no_plate = models.CharField(max_length=10)


class comp_drivers(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 91XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)


class comp_PresentWork(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE)
    driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='drivers')
    co_driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='codrivers')
    current_status = models.CharField(max_length=1024)


class comp_PastWork(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE)
    Rating = models.CharField(max_length=1024)
    driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='driver')
    co_driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='codriver')
    delivered_on = models.DateTimeField(auto_now_add=True)
