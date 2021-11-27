from datetime import datetime

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import View
from User.models import User_custom, Referral
from .forms import SignUpForm, adddriverForm, addTransportForm, PresentWorkSetForm, PresentWorkUpdateForm,Profile
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from .tokens import account_activation_token
from .models import patnerComp, Comp_profile, Comp_address, comp_Bids, comp_drivers, comp_PastWork, comp_PresentWork, \
    comp_Transport, shipJob_Saved, shipJob_jobanswer
from Customer.models import shipJob, Expired_ShipJob, Shipment_Related_Question, Customer_profile


# Create your views here.

class SignUpView(View):
    form_class = SignUpForm

    template_name = 'partner_company/signup.html'

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
                return redirect('partner_company:partner_company/login')
                # return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class SignUpVieww(View):
    form_class = SignUpForm

    template_name = 'account/signup.html'

    @classmethod
    def ref(self, request, uid, *args, **kwargs):
        form = self.form_class()
        # link = request.GET.get('ref=', None)
        return render(request, self.template_name, {'form': form, 'uid': uid})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(User_custom.objects.all())
        return render(request, self.template_name, {'form': form})

    def post(self, request, uid, *args, **kwargs):
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
                user.is_company = True  # Deactivate account till it is confirmed
                user.save()

                reff = Referral(referred_by_id=uid, user_id=user.pk)
                reff.save()
                new_candidate = patnerComp(user=user, is_email_verified=False)  # change is email to False after testing
                new_candidate.save()
                current_site = get_current_site(request)
                subject = 'Activate Your FinTop Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                # return redirect('login')
                return render(request, self.template_name, {'form': form})
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
            return redirect('partner_company:home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('partner_company:home')


def index(request):
    return render(request, 'index.html')


def login_candidate(request):
    if request.user.is_authenticated and request.user.is_company:
        print(request.user)
        return redirect('partner_company:partner_company_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            # print(username)
            # print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_company:
                login(request, user)
                return redirect('partner_company:partner_company_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'partner_company/login.html', context)


def partner_company_Home(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        jobs = []
        job_ques = []
        relevant_jobs = []
        common = []
        companyprofile = []
        job_skills = []
        u = request.user
        if u is not None and u.is_company:
            c = patnerComp.objects.get(user=u)
            try:
                cp = Comp_profile.objects.get(comp=c)
            except Comp_profile.DoesNotExist:
                cp = None
            try:
                cadd = Comp_address.objects.get(comp=c)
            except Comp_address.DoesNotExist:
                cadd = None
            try:
                cep = comp_PastWork.objects.filter(comp=c)
            except comp_PastWork.DoesNotExist:
                cep = None
            ncep = len(cep)
            print("ncep", ncep)
            if u.first_login:

                job = shipJob.objects.filter(bid_selected=False)
                print(job)
                for j in job:
                    start_date = j.created_on
                    # print(start_date)
                    today = datetime.now()
                    # print(type(today))
                    stat_date = str(start_date)
                    start_date = stat_date[:19]
                    tday = str(today)
                    today = tday[:19]
                    s_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                    e_date = datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
                    # print(s_date)
                    # print(e_date)
                    diff = abs((e_date - s_date).days)

                    if diff > 14:
                        Expired_ShipJob.objects.create(cust=j.cust, ship_title=j.ship_title,
                                                       job_description=j.job_description,
                                                       picking_Address=j.picking_Address,
                                                       droping_Address=j.droping_Address).save()

                        j.delete()

                    else:
                        jobs.append(j)

                for job in jobs:

                    e = job.cust
                    try:
                        c_p = Customer_profile.objects.get(cust=e)
                    except Customer_profile.DoesNotExist:
                        c_p = None
                    companyprofile.append(c_p)

                    try:
                        userS = shipJob_Saved.objects.get(job_id=job.pk, comp_id=c)
                        # print(userS.job_id)
                    except shipJob_Saved.DoesNotExist:
                        userS = None
                    try:
                        userA = comp_Bids.objects.get(job_id=job.pk, comp_id=c)
                        # print(userA.job_id)
                    except comp_Bids.DoesNotExist:
                        userA = None

                    if userA:
                        # print(userA)
                        continue
                    if userS:
                        # print(userS)
                        continue
                    relevant_jobs.append(job)
                    job_ques.append(Shipment_Related_Question.objects.filter(job_id=job))
                object2 = zip(relevant_jobs, job_ques, companyprofile)

                return render(request, 'partner_company/home.html',
                              {'jobs': object2, 'c': c, 'cp': cp, 'cep': cep,'n':ncep,'cadd':cadd})

            else:
                u.first_login = True
                u.save()
                return redirect('partner_company:create_profile')
        else:
            return redirect('/')

    if request.method == 'POST':
        print(request.POST)
        pk = request.POST.get('pk')
        print(pk)
        c = patnerComp.objects.get(user=request.user)
        job = shipJob.objects.get(pk=pk)
        questions = Shipment_Related_Question.objects.filter(job_id=job)
        for q in questions:
            print(request.POST.get(q.question))

            get_text = request.POST.get(q.question)
            print(get_text)
            shipJob_jobanswer.objects.create(candidate_id=c, question_id=q, answer=get_text).save()
        comp_Bids.objects.create(comp=c, job_id=job).save()


def save_later(request, pk):
    c = patnerComp.objects.get(user=request.user)
    if c is not None:
        job = shipJob.objects.get(pk=pk)
        # print(c)
        # print(job)
        shipJob_Saved.objects.create(job_id=job, comp=c).save()
        return redirect('partner_company:partner_company_home')
    else:
        return redirect('/')


def ProfileView(request):

        u = request.user
        c = patnerComp.objects.get(user=u)
        try:
            profile = Comp_profile.objects.get(comp=c)
        except Comp_profile.DoesNotExist:
            profile = None
        try:
            address = Comp_address.objects.get(comp=c)
        except Comp_address.DoesNotExist:
            address = None
        try:
            truck = comp_Transport.objects.filter(comp=c)
        except comp_Transport.DoesNotExist:
            truck = None
        try:
            driver = comp_drivers.objects.filter(comp=c)
        except comp_drivers.DoesNotExist:
            driver = None

        try:
            present_work = comp_PresentWork.objects.filter(comp=c)
        except comp_PresentWork.DoesNotExist:
            present_work = None
        try:
            past_work = comp_PastWork.objects.filter(comp=c)
        except comp_PastWork.DoesNotExist:
            past_work = None
        return render(request, 'partner_company/skills.html', {
            "user": u,
            "profile": profile,
            "address": address,
            "present_work": present_work,
            "past_work": past_work,
            "truck": truck,
            "driver": driver
        })


def ProfileEdit(request):
    user = request.user
    c = patnerComp.objects.get(user=request.user)
    if c is not None:
        try:
            cp = Comp_profile.objects.get(comp=c)
        except Comp_profile.DoesNotExist:
            cp=None
        if cp is None:
            if request.method == 'POST':
                form = Profile(request.POST or None,request.FILES or None)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.comp = c
                    f.save()
            form = Profile()
        else:
            if request.method == "POST":
                form = Profile(request.POST,request.FILES, instance=cp)
                if form.is_valid():
                    form.save()
                    return redirect('partner_company:profile')

            form = Profile(instance=cp)
        return render(request,'partner_company/EditProfile.html',{'form':form})
    else:
        return redirect('/')



def SavedJobs(request):

    jobs = []
    job_ques = []
    relevant_jobs = []
    common = []
    companyprofile = []
    job_skills = []
    u = request.user
    if u is not None and u.is_company:
        if request.method == 'POST':
            print(request.POST)
            pk = request.POST.get('pk')
            print(pk)
            c = patnerComp.objects.get(user=request.user)
            job = shipJob.objects.get(pk=pk)
            questions = Shipment_Related_Question.objects.filter(job_id=job)
            for q in questions:
                print(request.POST.get(q.question))

                get_text = request.POST.get(q.question)
                print(get_text)
                shipJob_jobanswer.objects.create(candidate_id=c, question_id=q, answer=get_text).save()
            comp_Bids.objects.create(comp=c, job_id=job).save()
        c = patnerComp.objects.get(user=u)
        try:
            cp = Comp_profile.objects.get(comp=c)
        except Comp_profile.DoesNotExist:
            cp = None
        try:
            cep = comp_PastWork.objects.filter(comp=c)
        except comp_PastWork.DoesNotExist:
            cep = None
        if u.first_login:
            job = shipJob_Saved.objects.filter(comp=c)
            print(job)
            for j in job:
                start_date = j.job_id.created_on
                # print(start_date)
                today = datetime.now()
                # print(type(today))
                stat_date = str(start_date)
                start_date = stat_date[:19]
                tday = str(today)
                today = tday[:19]
                s_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                e_date = datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
                # print(s_date)
                # print(e_date)
                diff = abs((e_date - s_date).days)
                print(diff)
                if diff > 30:
                    # expired_job.append(j)
                    Expired_ShipJob.objects.create(job_id=j.job_id).save()
                    j.delete()
                else:
                    jobs.append(j)
                    print(jobs)
            for job in jobs:
                e = job.job_id.cust
                companyprofile.append(Customer_profile.objects.get(cust=e))
                print(companyprofile)
                try:
                    userA = comp_Bids.objects.get(job_id=job.pk, comp=c)

                except comp_Bids.DoesNotExist:
                    userA = None
                print(userA)
                if userA is not None:
                    print(userA)

                else:
                    print(job)
                    relevant_jobs.append(job)
                    print(relevant_jobs)
                    job_ques.append(Shipment_Related_Question.objects.filter(job_id=job.job_id))
            object2 = zip(relevant_jobs, job_ques, companyprofile)
            return render(request, 'partner_company/savedjobs.html',
                          {'jobs': object2, 'c': c, 'cp': cp, 'cep': cep})
        else:
            u.first_login = True
            u.save()
            return redirect('partner_company:create_profile')
    else:
        return redirect('/')



def AppliedJobs(request):
    companyprofile = []
    user = request.user
    if user is not None and user.is_company:
        c = patnerComp.objects.get(user=request.user)
        try:
            cp = Comp_profile.objects.get(comp=c)
        except Comp_profile.DoesNotExist:
            cp = None
        applied = comp_Bids.objects.filter(comp=c)
        for a in applied:
            e = a.job_id.cust
            companyprofile.append(Customer_profile.objects.get(cust=e))

        objects = zip(applied, companyprofile)

        return render(request, 'partner_company/applied.html',
                      {'jobs': objects, 'c': c, 'cp': cp})
        # objects = zip(applied, companyprofile)
        # return render(request, 'partner_company/applied.html', {'jobs': objects, 'cp': cp})
    else:
        return redirect('/')


def remove_applied(request, pk):
    comp_Bids.objects.get(pk=pk).delete()

    return redirect('partner_company:AppliedJobs')


def remove_saved(request, pk):
    c = patnerComp.objects.get(user=request.user)
    # job = shipJob.objects.get(pk=pk)
    savej = shipJob_Saved.objects.filter(pk=pk)
    for s in savej:
        if s.comp == c:
            s.delete()

    return redirect('partner_company:SavedJobs')


def addTransport(request):
    user = request.user
    if user.is_company:
        pr = patnerComp.objects.get(user=user)
        try:
            cp = Comp_profile.objects.get(comp=pr)
            if request.method == 'POST':
                form = addTransportForm(data=request.POST or None)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.comp = pr
                    f.save()
                    messages.success(request, 'Transport is added.')
            form = addTransportForm()
            return render(request, 'partner_company/addTransport.html',
                          {'form': form,'cp':cp})
        except Comp_profile.DoesNotExist:
            return redirect('partner_company:create_profile')
    else:
        return redirect('/')


def addDriver(request):
    user = request.user
    if user.is_company:
        pr = patnerComp.objects.get(user=user)
        try:
            cp = Comp_profile.objects.get(comp=pr)
            if request.method == 'POST':
                form = adddriverForm(data=request.POST or None)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.comp = pr
                    f.save()
                    messages.success(request, 'Driver is added.')
            form = adddriverForm()
            return render(request, 'partner_company/adddriver.html',
                          {'form': form,'cp':cp})
        except Comp_profile.DoesNotExist:
            return redirect('partner_company:create_profile')
    else:
        return redirect('/')


def SetUp_PresentShip(request, pk):
    user = request.user
    if user.is_company:
        pr = patnerComp.objects.get(user=user)
        job = shipJob.objects.get(pk=pk)
        if request.method == 'POST':
            form = PresentWorkSetForm(data=request.POST or None)
            if form.is_valid():
                f = form.save(commit=False)
                f.comp = pr
                f.job_id = job
                f.current_status = "Driver and Truck assigned"
                f.save()
            return redirect('partner_company:partner_company_home')
        form = PresentWorkSetForm()
        return render(request, 'partner_company/setup_presentShip.html',
                      {'form': form})
    else:
        return redirect('/')


def Update_PresentShip(request, pk):
    user = request.user
    if user.is_company:
        pr = patnerComp.objects.get(user=user)
        job = get_object_or_404(shipJob, pk=pk)
        if request.method == 'POST':
            form = PresentWorkUpdateForm(request.POST, instance=job)
            if form.is_valid():
                f = form.save(commit=False)
                f.comp = pr
                f.job_id = job
                f.save()
            return redirect('partner_company:partner_company_home')
        form = PresentWorkUpdateForm(instance=job)
        return render(request, 'partner_company/setup_presentship.html',
                      {'form': form})
    else:
        return redirect('/')
def PresentShip(request):
    profile = []
    user = request.user
    if user.is_company:
        pr = patnerComp.objects.get(user=user)
        c = comp_PresentWork.objects.filter(comp=pr)
        for cp  in c:
            profile.append(Customer_profile.objects.get(cust=cp.cust))
        o = zip(c,profile)
        return render(request,'partner_company/ShipmentOngoing.html',{'c_p':o})
    else:
       return redirect('/')
def ManageDriver(request):
    user=request.user
    cp=[]
    if user.is_company:
        comp = patnerComp.objects.get(user=user)
        drivers = comp_drivers.objects.filter(comp=comp)
        for d in drivers:
            try:
                cp.append(comp_PresentWork.objects.filter(driver=d))
            except comp_PresentWork.DoesNotExist:
                c.append(None)
        info = zip(drivers,cp)
        return render(request, 'partner_company/DriverManagement.html', {'info': info})
    else:
        return redirect('/')
def ManageTruck(request):
    user=request.user
    cp=[]
    if user.is_company:
        comp = patnerComp.objects.get(user=user)
        Trucks = comp_Transport.objects.filter(comp=comp)
        for d in Trucks:
            try:
                cp.append(comp_PresentWork.objects.filter(transport=d))
            except comp_PresentWork.DoesNotExist:
                c.append(None)
        info = zip(Trucks,cp)
        return render(request, 'partner_company/TransprtManagement.html', {'info': info})
    else:
        return redirect('/')
def DriverRecords(request):
    user=request.user
    cp=[]
    n=[]
    if user.is_company:
        comp = patnerComp.objects.get(user=user)
        drivers = comp_drivers.objects.filter(comp=comp)
        for d in drivers:
            try:
                cp.append(comp_PastWork.objects.filter(driver=d))
                n.append(len(comp_PastWork.objects.filter(driver=d)))
            except comp_PastWork.DoesNotExist:
                c.append(None)
        info = zip(drivers,cp,n)
        return render(request, 'partner_company/DriverPastwork.html', {'info': info})
    else:
        return redirect('/')
def RemoveDriver(request, pk):
    comp_drivers.objects.get(pk=pk).delete()

    return redirect('partner_company:ManageDriver')
def RemoveTruck(request, pk):
    comp_Transport.objects.get(pk=pk).delete()

    return redirect('partner_company:ManageTruck')