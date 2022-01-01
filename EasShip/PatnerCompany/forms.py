from django import forms
from django.contrib.auth.forms import UserCreationForm
from User.models import User_custom
from .models import comp_Transport, comp_drivers, comp_PresentWork, Comp_profile
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
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
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


class adddriverForm(forms.ModelForm):
    name = forms.CharField(label='Name of the new Driver', max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': "input100"}))
    phone = forms.CharField(label='Phone of the new Driver', max_length=30, required=True, widget=forms.NumberInput(
        attrs={'class': "input100"}))

    class Meta:
        model = comp_drivers
        fields = [
            'name',
            'phone',
        ]


class addTransportForm(forms.ModelForm):
    type_of_transport = forms.CharField(label='Type of the Vehicle', max_length=30, required=True,
                                        widget=forms.TextInput(
                                            attrs={'class': "input100"}))
    
    transport_no_plate = forms.CharField(label='Vehicle Plate Number', max_length=30, required=True,
                                         widget=forms.TextInput(
                                             attrs={'class': "input100"}))

    class Meta:
        model = comp_Transport
        fields = [
            'type_of_transport',
            'transport_no_plate',
        ]


class PresentWorkSetForm(forms.ModelForm):
    class Meta:
        model = comp_PresentWork
        fields = [
            'driver',
            'co_driver',
            'transport',

        ]


class PresentWorkUpdateForm(forms.ModelForm):
    


    class Meta:
        model = comp_PresentWork
        fields = [
            'driver',
            'co_driver',
            'transport',
            'current_status',
            
        ]


class Profile(forms.ModelForm):
    company_name = forms.CharField(label='Enter name of company', max_length=30, required=True,
                                        widget=forms.TextInput(
                                            attrs={'class': "input100"}))
    company_type = forms.CharField(label='Enter Type  of company', max_length=30, required=True,
                                   widget=forms.TextInput(
                                       attrs={'class': "input100"}))
    phone = forms.CharField(label='Phone of the Company', max_length=30, required=True, widget=forms.NumberInput(
        attrs={'class': "input100"}))

    class Meta:
        model = Comp_profile
        fields = [
            'company_logo',
            'company_name',
            'company_type',
            'phone'
        ]
