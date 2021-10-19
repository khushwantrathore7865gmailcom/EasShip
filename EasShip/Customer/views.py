from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from User.models import User_custom, Referral, Commission_request
from .forms import SignUpForm, ShipJob, prod_Detail_Formset
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from .tokens import account_activation_token
from .models import customer, Customer_address, Customer_profile, ProdDesc, shipJob, Expired_ShipJob, \
    Shipment_Related_Question
from PatnerCompany.models import shipJob_jobanswer, comp_Bids, Comp_address, Comp_profile, comp_Transport, \
    comp_PresentWork, comp_PastWork, comp_drivers


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
                user.is_customer = True  # Deactivate account till it is confirmed
                user.save()

                reff = Referral(referred_by_id=uid, user_id=user.pk)
                reff.save()
                new_candidate = customer(user=user, is_email_verified=False)  # change is email to False after testing
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
    jobs = []
    expired_job = []
    user = request.user
    if user is not None and user.is_customer:
        try:
            e = customer.objects.get(user=user)
        except customer.DoesNotExist:
            e = None
        # uncomment this after making the profile update correct
        # if Employer_profile.objects.get(employer=e):
        if e:
            try:
                ep = Customer_profile.objects.get(cust=e)
            except Customer_profile.DoesNotExist:
                ep = None
            job = shipJob.objects.filter(cust=e)
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
                print(diff)
                try:
                    e_j = Expired_ShipJob.objects.get(job_id=j)
                except Expired_ShipJob.DoesNotExist:
                    e_j = None
                if diff > 30:
                    if e_j:
                        expired_job.append(j)

                    else:
                        Expired_ShipJob.objects.create(job_id=j).save()
                        expired_job.append(j)
                elif e_j:
                    expired_job.append(j)
                else:
                    jobs.append(j)
            context = {'jobs': jobs, 'expired': expired_job, 'ep': ep}
            return render(request, 'customer/job-post.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')
    # user = request.user
    # try:
    #     e = customer.objects.get(user=user)
    # except customer.DoesNotExist:
    #     e = None
    # if e:
    #     j = shipJob.objects.filter(cust=e)
    #
    #     context = {
    #         'user': e,
    #         'jobs': j,
    #     }
    #     return render(request, 'customer/home.html', context)
    # else:
    #     return redirect('/')


def Add_Shipment(request):
    u = request.user
    if u is not None and u.is_customer:
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
        return render(request, 'customer/addjob.html', {'form': form})
    else:
        return redirect('/')


def unpublish(request, pk):
    user = request.user
    job = shipJob.objects.get(pk=pk)
    # print(c)
    # print(job)
    Expired_ShipJob.objects.create(job_id=job).save()
    return redirect('recruiter:employer_home')


def remove_unpublish(request, pk):
    job = shipJob.objects.get(pk=pk)
    unpub_job = Expired_ShipJob.objects.get(job_id=job)
    unpub_job.delete()
    job.created_on = datetime.now()
    job.save()

    return redirect('recruiter:employer_home')


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


def job_detail(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        e = customer.objects.get(user=request.user)
        job = shipJob.objects.get(pk=pk)
        company = Customer_profile.objects.get(cust=e)
        # candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
        # objects = zip(job,candidate_Applied)
        return render(request, 'customer/job_details.html', {'job': job, 'c': company})
    else:
        return redirect('/')


@login_required(login_url='/')
def view_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        candidate_user = []
        candidate_profile = []
        address_profile = []
        professional_profile = []

        candidate_answer = []
        # Question=[]
        e = customer.objects.get(user=request.user)

        cp = Customer_profile.objects.get(cust=e)
        job = shipJob.objects.get(pk=pk)

        question = Shipment_Related_Question.objects.filter(job_id=job)
        candidate_Applied = comp_Bids.objects.filter(job_id=job)
        for can in candidate_Applied:
            c = can.comp
            c_p = Comp_profile.objects.get(comp=c)
            c_e = Comp_address.objects.get(comp=c)
            p_p = comp_PastWork.objects.filter(comp=c)
            candidate_profile.append(c_p)
            print("working filter")
            print(candidate_profile)
            candidate_user.append(c.user)
            address_profile.append(c_e)
            professional_profile.append(p_p)

            for q in question:
                candidate_answer.append(
                    shipJob_jobanswer.objects.get(question_id=q, candidate_id=c))

        quest = zip(question, candidate_answer)
        # print(candidate_answer)
        objects = zip(candidate_profile, address_profile, professional_profile,
                      candidate_user, candidate_Applied)

        return render(request, 'employer/job_candidate.html',
                      {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer, 'cp': cp})
        # return render(request, 'employer/job_candidate.html',
        #               {'candidate': objects, 'job': job, 'quest': quest})
    else:
        return redirect('/')


@login_required(login_url='/')
def shortlistview_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        e = customer.objects.get(user=user)
        cp = Customer_profile.objects.get(employer=e)
        candidate_user = []
        candidate_profile = []
        address_profile = []
        professional_profile = []

        candidate_answer = []

        job = ShipJob.objects.get(pk=pk)
        question = Shipment_Related_Question.objects.filter(job_id=job)
        candidate_Applied = comp_Bids.objects.filter(job_id=job)
        for can in candidate_Applied:
            c = can.candidate_id
            candidate_profile.append(Comp_profile.objects.get(comp=c))
            candidate_user.append(c.user)
            address_profile.append(Comp_address.objects.filter(comp=c))
            professional_profile.append(comp_PastWork.objects.filter(comp=c))

            for q in question:
                candidate_answer.append(shipJob_jobanswer.objects.get(question_id=q, candidate_id=c))

        objects = zip(candidate_profile, address_profile, professional_profile,
                      candidate_user, candidate_Applied)
        # question = zip(question, candidate_answer)
        return render(request, 'employer/shortlisted_view.html',
                      {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer, 'cp': cp})
    else:
        return redirect('/')


@login_required(login_url='/')
def disqualifyview_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        e = customer.objects.get(user=user)
        cp = Customer_profile.objects.get(employer=e)
        candidate_user = []
        candidate_profile = []
        address_profile = []
        professional_profile = []

        candidate_answer = []

        job = ShipJob.objects.get(pk=pk)
        question = Shipment_Related_Question.objects.filter(job_id=job)
        candidate_Applied = comp_Bids.objects.filter(job_id=job)
        for can in candidate_Applied:
            c = can.candidate_id
            candidate_profile.append(Comp_profile.objects.get(comp=c))
            candidate_user.append(c.user)
            address_profile.append(Comp_address.objects.filter(comp=c))
            professional_profile.append(comp_PastWork.objects.filter(comp=c))

            for q in question:
                candidate_answer.append(shipJob_jobanswer.objects.get(question_id=q, candidate_id=c))

        objects = zip(candidate_profile, address_profile, professional_profile,
                      candidate_user, candidate_Applied)

        # question = zip(question, candidate_answer)
        return render(request, 'employer/disqualified.html',
                      {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer, 'cp': cp})
    else:
        return redirect('/')


@login_required(login_url='/')
def shortlist(request, pk):
    e = comp_Bids.objects.get(pk=pk)
    e.is_shortlisted = True
    e.is_disqualified = False
    e.save()
    print(e.job_id.pk)
    return redirect('recruiter:view_applied_candidate', e.job_id.pk)


@login_required(login_url='/')
def disqualify(request, pk):
    e = comp_Bids.objects.get(pk=pk)
    e.is_shortlisted = False
    e.is_disqualified = True
    e.save()
    print(e.job_id.pk)
    return redirect('recruiter:view_applied_candidate', e.job_id.pk)


@login_required(login_url='/')
def delete_job(request, pk):
    ShipJob.objects.get(pk=pk).delete()

    return redirect('recruiter:employer_home')


@login_required(login_url='/')
def publish_job(request, pk):
    e = ShipJob.objects.get(pk=pk)
    e.is_save_later = False
    e.save()
    return redirect('recruiter:job_detail', pk)


@login_required(login_url='/')
def ProfileView(request):
    u = request.user
    e = customer.objects.get(user=u)
    profile = Customer_profile.objects.get(employer=e)

    return render(request, 'employer/skills.html', {
        "user": u,
        "profile": profile,

    })


@login_required(login_url='/')
def job_Response(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        job = ShipJob.objects.get(pk=pk)
        response = comp_Bids.objects.filter(job_id=job)
        return render(request, 'dashboard/jobresponse.html', {'response': response})
    else:
        return redirect('/')


# TODO:and request page for money
def Request_commision(request):
    user = request.user
    if user is not None and user.is_customer:
        Commission_request.objects.create(user=user).save()
        return redirect('customer:Commission')
    else:
        return redirect('/')


def Commission_View(request):
    user = request.user
    if user is not None and user.is_customer:
        total = 0
        re = Referral.objects.filter(referred_by=user)
        for r in re:
            total = total + r.commissions
        return render(request, 'customer/Commission_view.html', {'com': total, 'referred': re})
    else:
        return redirect('/')
