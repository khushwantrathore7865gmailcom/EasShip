from django.shortcuts import render, redirect
from User.models import Referral, Commission_request
from django.contrib.auth.decorators import login_required
from PatnerCompany.models import patnerComp, Comp_profile
from Customer.models import customer, Customer_profile

from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
@login_required(login_url='/')
def Referal_view(request):
    user = request.user
    Refered = Referral.objects.filter(referred_by=user)
    ref = []
    total_commission = 0
    for r in Refered:

        if r.no_of_jobdone < 6:
            ref.append(r)
            total_commission = total_commission + r.commissions
    user_profile = []
    for r in ref:
        u = r.user
        if u.is_company:
            comp = patnerComp.objects.get(user=u)
            user_profile.append(Comp_profile.objects.get(comp=comp))
        else:
            cust = customer.objects.get(user=u)
            user_profile.append(Customer_profile.objects.get(cust=cust))
    object = zip(ref, user_profile)
    if user.is_company:
        p = True
        comp = patnerComp.objects.get(user=user)
        c = Comp_profile.objects.get(comp=comp)
    else:
        p = False
        cust = customer.objects.get(user=user)
        c = Customer_profile.objects.get(cust=cust)
    return render(request, 'referal/refered.html', {'referedto': object, 'p': p, 'c': c, 't': total_commission})


def request_payment(request, pk):
    user = request.user
    r = Referral.objects.get(pk=pk)
    c = Commission_request(Refer=r, requested_completed=False).save()

    subject = 'Commission Request'
    message = f'Commission Request is asked by  {r}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['khushwantrathore7865@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('Referview:referal')
