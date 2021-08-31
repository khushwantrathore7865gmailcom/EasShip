from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from User.models import User_custom
from .forms import SignUpForm, ShipJob, prod_Detail_Formset
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from .tokens import account_activation_token
from .models import customer, Customer_address, Customer_profile, ProdDesc, shipJob


# Create your views here.

class SignUpView(View):
    form_class = SignUpForm

    template_name = 'customer/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(User_custom.objects.all())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            emaill = form.cleaned_data['email']
            if User_custom.objects.filter(email=emaill).exists():

                return HttpResponse('User with same email already exists, Please try again with different Username!!')
            else:
                user = form.save(commit=False)
                user.username = user.email
                user.user_name = user.email
                user.is_active = True  # change this to False after testing
                user.is_customer = True
                user.save()
                new_candidate = customer(user=user, is_email_verified=False)  # change is email to False after testing
                new_candidate.save()
                current_site = get_current_site(request)
                # subject = 'Activate Your WorkAdaptar Account'
                # message = render_to_string('emails/account_activation_email.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': account_activation_token.make_token(user),
                # })
                # user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                return redirect('customer:customer/login')
                # return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User_custom.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User_custom.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True

            pr = customer.objects.get(user=user)
            pr.is_email_verified = True
            pr.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('customer:home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('customer:home')


def index(request):
    return render(request, 'index.html')


def login_candidate(request):
    if request.user.is_authenticated and request.user.is_customer:
        print(request.user)
        return redirect('customer:customer_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            # print(username)
            # print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_customer:
                login(request, user)
                return redirect('customer:customer_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'customer/login.html', context)


def customer_home(request):
    user = request.user
    try:
        e = customer.objects.get(user=user)
    except customer.DoesNotExist:
        e = None
    if e:
        j=shipJob.objects.filter(cust=e)
    context = {
        'user': e,
        'jobs':j,
    }
    return render(request, 'customer/home.html', context)


def Add_Shipment(request):
    u = request.user
    users = customer.objects.get(user=u)
    form = ShipJob()
    if request.method == 'POST':
        form = ShipJob(request.POST)
        f = form.save(commit=False)
        f.cust = users

        f.save()
        pk = f.pk
        print(pk)
        return redirect('customer:Add_prod_desc', pk)
    return render(request, 'customer/add_job.html', {'form': form})


def Add_prod_desc(request, pk):
    u = request.user
    ship = shipJob.objects.get(pk=pk)
    form = prod_Detail_Formset(request.GET or None)
    if request.method == 'POST':
        form = prod_Detail_Formset(request.POST)
        if form.is_valid:
            for f in form:
                print(f)
                prod_box = f.cleaned_data.get('prod_box')
                print(prod_box)
                prod_in_box = f.cleaned_data.get('prod_in_box')
                Weight_box = f.cleaned_data.get('Weight_box')
                length = f.cleaned_data.get('length')
                width = f.cleaned_data.get('width')
                height = f.cleaned_data.get('height')
                if prod_box:
                    ProdDesc(shipment=ship, prod_box=prod_box, prod_in_box=prod_in_box, Weight_box=Weight_box,
                             length=length, width=width, height=height).save()
            return redirect('customer:customer_home')

    return render(request, 'customer/add_job_desc.html', {"form2": form})
