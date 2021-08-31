from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from User.models import User_custom
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from .tokens import account_activation_token
from .models import patnerComp, Comp_profile, Comp_address, comp_Bids, comp_drivers, comp_PastWork, comp_PresentWork, \
    comp_Transport


# Create your views here.

class SignUpView(View):
    form_class = SignUpForm

    template_name = 'patner_company/signup.html'

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
                user.is_company = True
                user.save()
                new_candidate = patnerComp(user=user, is_email_verified=False)  # change is email to False after testing
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

            pr = patnerComp.objects.get(user=user)
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
    if request.user.is_authenticated and request.user.is_company:
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
        return render(request, 'patner_company/login.html', context)


def partner_company_home(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'partner_company/home.html', context)
