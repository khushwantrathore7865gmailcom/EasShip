from django.db import models
from User.models import User_custom
from django.core.validators import RegexValidator
from Customer.models import shipJob, Shipment_Related_Question,Expired_ShipJob


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

    company_type = models.CharField(max_length=250, blank=True, )
    company_name = models.CharField(max_length=250, blank=True, )
    company_logo = models.ImageField(blank=True,upload_to="company_logo/",default="profile.png" )

    def __str__(self):
        return f"{self.comp.user.username}-{self.company_name}"


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

    def __str__(self):
        return f"{self.comp.user.username}-{self.city}"
#
class comp_Transport(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    type_of_transport = models.CharField(max_length=1024)
    
    transport_no_plate = models.CharField(max_length=13,unique=True)
    def __str__(self):
        return f"{self.transport_no_plate}-{self.type_of_transport}"

class comp_drivers(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    user = models.ForeignKey(User_custom,null=True,on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=1024)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 91XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    def __str__(self):
        return f"{self.name}-{self.phone}"


class shipJob_jobanswer(models.Model):
    candidate_id = models.ForeignKey(patnerComp, models.CASCADE)
    # employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Shipment_Related_Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1250)



class comp_Bids(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE, db_constraint=False)
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE, db_constraint=False)
    Bid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2)
    Bid_byPartner = models.DecimalField(
        max_digits=12,
        decimal_places=2, null=True)
    complete_in = models.IntegerField()
    bid_on = models.DateTimeField(auto_now_add=True)
    is_shortlisted = models.BooleanField(default=False)
    is_disqualified = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    completed_shipment = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.comp.user.username}-{self.job_id}is {self.is_selected}"


class shipJob_Saved(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.comp.user.username}-{self.job_id}"

class comp_PresentWork(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    job_id = models.ForeignKey(shipJob, on_delete=models.CASCADE)
    driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='drivers')
    co_driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='codrivers',blank=True,null=True)
    transport = models.ForeignKey(comp_Transport, on_delete=models.CASCADE, related_name='transports')
    current_status = models.CharField(max_length=1024)
    Total_payment = models.ForeignKey(comp_Bids, on_delete=models.CASCADE)
    payment_Done = models.DecimalField(
        max_digits=12,
        decimal_places=2, null=True)
    Payment_complete = models.BooleanField(default=False)
    ask_finalpay = models.BooleanField(default=False)
    request_update = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.comp.user.username}-{self.job_id}-{self.driver}"


class comp_PastWork(models.Model):
    comp = models.ForeignKey(patnerComp, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Expired_ShipJob, on_delete=models.CASCADE)
    Rating = models.IntegerField(max_length=1024)
    Bid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,null=True)
    Bid_byPartner = models.DecimalField(
        max_digits=12,
        decimal_places=2, null=True)
    driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='driver')
    co_driver = models.ForeignKey(comp_drivers, on_delete=models.CASCADE, related_name='codriver',blank=True,null=True)
    transport = models.ForeignKey(comp_Transport, on_delete=models.CASCADE, related_name='transport')
    delivered_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.comp.user.username}-{self.job_id}-{self.Rating}"


class Orders(models.Model):
    order_id = models.CharField(max_length=5000, null=True)
    work = models.ForeignKey(comp_PresentWork, on_delete=models.CASCADE)
    order_done = models.CharField(max_length=5000, null=True)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2, null=True)
    def __str__(self):
        return f"{self.work.comp.user.username}-{self.order_id}is {self.order_done}"