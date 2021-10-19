from django.db import models

from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class User_custom(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    # password = models.CharField(max_length=32,widget=forms.PasswordInput)
    password = models.CharField(max_length=32)
    confirmpass = models.CharField(max_length=32, blank=True)
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    first_login = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_name


class Referral(models.Model):
    referred_by = models.ForeignKey(User_custom, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User_custom, on_delete=models.CASCADE, related_name='+')
    status = models.CharField(max_length=15, null=True, blank=True)
    commissions = models.CharField(max_length=20)
    commission_status = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)


class Commission_request(models.Model):
    user = models.ForeignKey(User_custom, on_delete=models.CASCADE, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True)
    Error = models.CharField(max_length=1025)
    requested_completed = models.BooleanField(default=False)
