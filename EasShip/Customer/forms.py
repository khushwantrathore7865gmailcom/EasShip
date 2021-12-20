from django import forms
from django.contrib.auth.forms import UserCreationForm
from User.models import User_custom, Commission_request
from .models import shipJob, ProdDesc, Customer_profile
from django.forms import formset_factory
from django.forms import modelformset_factory

job_Type = [
    ('Part time', 'Part time'),
    ('Full time', 'Full time'),
    ('Internship', 'Internship'),
]
Gender = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]
state_choices = (("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), ("Assam", "Assam"),
                 ("Bihar", "Bihar"), ("Chhattisgarh", "Chhattisgarh"), ("Goa", "Goa"), ("Gujarat", "Gujarat"),
                 ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"),
                 ("Jammu and Kashmir ", "Jammu and Kashmir "), ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"),
                 ("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"), ("Maharashtra", "Maharashtra"),
                 ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"), ("Nagaland", "Nagaland"),
                 ("Odisha", "Odisha"), ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"), ("Sikkim", "Sikkim"),
                 ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), ("Tripura", "Tripura"),
                 ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), ("West Bengal", "West Bengal"),
                 ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), ("Chandigarh", "Chandigarh"),
                 ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), ("Daman and Diu", "Daman and Diu"),
                 ("Lakshadweep", "Lakshadweep"),
                 ("National Capital Territory of Delhi", "National Capital Territory of Delhi"),
                 ("Puducherry", "Puducherry"))
Martial_Status = [
    ('Single', 'Single'),
    ('Married ', 'Married'),
]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your first name', 'class': "input100"}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your first name', 'class': "input100"}))
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter email address', 'class': "input100"}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password ', 'class': "input100"}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'confirm Password ', 'class': "input100"}))

    class Meta:
        model = User_custom
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class ShipJob(forms.ModelForm):
    ship_title = forms.CharField(label='Title of your New Shipment', max_length=30, required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': "input100"}))
    job_description = forms.CharField(
        label='Enter the description about the shipment (do mention if shipment is fragile)', max_length=30,
        required=False, widget=forms.TextInput(
            attrs={'class': "input100"}))
    picking_Address = forms.CharField(label='Enter the address from where to pick the shipment', max_length=30,
                                      required=False, widget=forms.Textarea(
            attrs={'class': "input100"}))
    droping_Address = forms.CharField(label='Enter the address where to drop the shipment', max_length=30,
                                      required=False, widget=forms.Textarea(
            attrs={'class': "input100"}))

    class Meta:
        model = shipJob
        fields = [
            'ship_title',
            'job_description',
            'picking_Address',
            'droping_Address',
        ]


class Prod_Detail(forms.ModelForm):
    value = forms.CharField(
        label='Value of Shipment',
        widget=forms.TextInput(attrs={
            'class': 'form-control input100',
            'placeholder': 'Estimated value of shipment'
        })
    )

    Weight_box = forms.CharField(
        label='Weight of box(in kg)',
        widget=forms.TextInput(attrs={
            'class': 'form-control input100',
            'placeholder': 'weight of Shipment'
        })
    )
    length = forms.CharField(
        label='Length of Shipment(in meter)',
        widget=forms.TextInput(attrs={
            'class': 'form-control input100',
            'placeholder': 'Length of Shipment'
        })
    )
    width = forms.CharField(
        label='Width of Shipment(in meter)',
        widget=forms.TextInput(attrs={
            'class': 'form-control input100',
            'placeholder': 'Width of Shipment'
        })
    )
    height = forms.CharField(
        label='Height of Shipment(in meter)',
        widget=forms.TextInput(attrs={
            'class': 'form-control input100',
            'placeholder': 'Height of Shipment'
        })
    )

    class Meta:
        model = ProdDesc
        fields = [
            'value',
            'Weight_box',
            'length',
            'width',
            'height'
        ]


class Profile(forms.ModelForm):
    class Meta:
        model = Customer_profile
        fields = [
            'company_logo',
            'company_name',
            'company_type',
            'phone',
            'address'
        ]
