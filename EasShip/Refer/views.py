from django.shortcuts import render
from User.models import Referral, Commission_request
from django.contrib.auth.decorators import login_required
from PatnerCompany.models import patnerComp,Comp_profile
from Customer.models import customer,Customer_profile
# Create your views here.
@login_required(login_url='/')
def Referal_view(request):
    user = request.user
    Refered = Referral.objects.filter(referred_by=user)

    if user.is_company:
        p = True
        comp = patnerComp.objects.get(user=user)
        c = Comp_profile.objects.get(comp=comp)
    else:
        p = False
        cust = customer.objects.get(user=user)
        c= Customer_profile.objects.get(cust=cust)
    return render(request, 'referal/refered.html', {'referedby': Refered, 'p': p,'c':c})
