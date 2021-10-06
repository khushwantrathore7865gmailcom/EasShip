from datetime import datetime

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
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
    comp_Transport, shipJob_Saved, shipJob_jobanswer
from Customer.models import shipJob, Expired_ShipJob, Shipment_Related_Question, Customer_profile


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
                user.is_C = True
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
        return render(request, 'customer/login.html', context)


def partner_company_home(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = shipJob.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
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
                    cp = Comp_profile.objects.get(user_id=c)
                except Comp_profile.DoesNotExist:
                    cp = None
                try:
                    cep = comp_PastWork.objects.get(user_id=c)
                except comp_PastWork.DoesNotExist:
                    cep = None

                if u.first_login:
                    print("len job")
                    print(len(job))
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
                        # print(diff)
                        if diff > 30:
                            # expired_job.append(j)
                            Expired_ShipJob.objects.create(job_id=j).save()

                        else:
                            jobs.append(j)
                        print("len")
                        print(len(jobs))
                    for jo in jobs:

                        e = jo.cust
                        companyprofile.append(Customer_profile.objects.get(comp=e))
                        try:
                            userS = shipJob_Saved.objects.get(job_id=jo.pk, comp=c)
                            # print(userS.job_id)
                        except shipJob_Saved.DoesNotExist:
                            userS = None
                        try:
                            userA = comp_Bids.objects.get(job_id=jo.pk, comp=c)
                            # print(userA.job_id)
                        except comp_Bids.DoesNotExist:
                            userA = None

                        if userA:
                            # print(userA)
                            continue
                        if userS:
                            # print(userS)
                            continue
                        relevant_jobs.append(jo)
                        print("job:")
                        print(jo)

                        job_ques.append(Shipment_Related_Question.objects.filter(job_id=jo))
                    print("job_quest:")
                    print(job_ques)
                    print("relevant_jobs")
                    print(len(relevant_jobs))
                    pj = Paginator(relevant_jobs, 5)
                    pjt = Paginator(relevant_jobs, 5)
                    pc = Paginator(common, 5)
                    pjs = Paginator(job_skills, 5)
                    pjq = Paginator(job_ques, 5)
                    pcp = Paginator(companyprofile, 5)
                    page_num = request.GET.get('page', 1)
                    try:
                        pj_objects = pj.page(page_num)
                        pjt_objects = pjt.page(page_num)
                        pc_objects = pc.page(page_num)
                        pjs_objects = pjs.page(page_num)
                        pjq_objects = pjq.page(page_num)
                        pcp_objects = pcp.page(page_num)
                    except EmptyPage:
                        pj_objects = pj.page(1)
                        pjt_objects = pjt.page(1)
                        pc_objects = pc.page(1)
                        pjs_objects = pjs.page(1)
                        pjq_objects = pjq.page(1)
                        pcp_objects = pcp.page(1)
                    objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                    return render(request, 'jobseeker/home.html',
                                  {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'pjs': pjt_objects})
                else:
                    u.first_login = True
                    u.save()
                    return redirect('jobseeker:create_profile')
            else:
                return redirect('/')

        else:
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
                    cp = Comp_profile.objects.get(user_id=c)
                except Comp_profile.DoesNotExist:
                    cp = None
                try:
                    cep = comp_PastWork.objects.get(user_id=c)
                except comp_PastWork.DoesNotExist:
                    cep = None
                if u.first_login:

                    job = shipJob.objects.all()
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
                        if diff > 30:
                            # expired_job.append(j)
                            Expired_ShipJob.objects.create(job_id=j).save()

                        else:
                            jobs.append(j)

                    for job in jobs:

                        e = job.cust
                        companyprofile.append(Customer_profile.objects.get(employer=e))
                        try:
                            userS = shipJob_Saved.objects.get(job_id=job.pk, candidate_id=c)
                            # print(userS.job_id)
                        except shipJob_Saved.DoesNotExist:
                            userS = None
                        try:
                            userA = comp_Bids.objects.get(job_id=job.pk, candidate_id=c)
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
                    pj = Paginator(relevant_jobs, 5)
                    pjt = Paginator(relevant_jobs, 5)
                    pc = Paginator(common, 5)
                    pjs = Paginator(job_skills, 5)
                    pjq = Paginator(job_ques, 5)
                    pcp = Paginator(companyprofile, 5)
                    page_num = request.GET.get('page', 1)
                    try:
                        pj_objects = pj.page(page_num)
                        pjt_objects = pjt.page(page_num)
                        pc_objects = pc.page(page_num)
                        pjs_objects = pjs.page(page_num)
                        pjq_objects = pjq.page(page_num)
                        pcp_objects = pcp.page(page_num)
                    except EmptyPage:
                        pj_objects = pj.page(1)
                        pjt_objects = pjt.page(1)
                        pc_objects = pc.page(1)
                        pjs_objects = pjs.page(1)
                        pjq_objects = pjq.page(1)
                        pcp_objects = pcp.page(1)
                    objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                    return render(request, 'jobseeker/home.html',
                                  {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'pjs': pjt_objects})

                else:
                    u.first_login = True
                    u.save()
                    return redirect('jobseeker:create_profile')
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
        shipJob_Saved.objects.create(job_id=job, candidate_id=c).save()
        return redirect('jobseeker:jobseeker_home')
    else:
        return redirect('/')


def ProfileView(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = shipJob.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
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
                    cp = Comp_profile.objects.get(user_id=c)
                except Comp_profile.DoesNotExist:
                    cp = None
                try:
                    cep = comp_PastWork.objects.get(user_id=c)
                except comp_PastWork.DoesNotExist:
                    cep = None

                if u.first_login:
                    print("len job")
                    print(len(job))
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
                        # print(diff)
                        if diff > 30:
                            # expired_job.append(j)
                            Expired_ShipJob.objects.create(job_id=j).save()

                        else:
                            jobs.append(j)
                        print("len")
                        print(len(jobs))
                    for jo in jobs:

                        e = jo.cust
                        companyprofile.append(Customer_profile.objects.get(comp=e))
                        try:
                            userS = shipJob_Saved.objects.get(job_id=jo.pk, comp=c)
                            # print(userS.job_id)
                        except shipJob_Saved.DoesNotExist:
                            userS = None
                        try:
                            userA = comp_Bids.objects.get(job_id=jo.pk, comp=c)
                            # print(userA.job_id)
                        except comp_Bids.DoesNotExist:
                            userA = None

                        if userA:
                            # print(userA)
                            continue
                        if userS:
                            # print(userS)
                            continue
                        relevant_jobs.append(jo)
                        print("job:")
                        print(jo)

                        job_ques.append(Shipment_Related_Question.objects.filter(job_id=jo))
                    print("job_quest:")
                    print(job_ques)
                    print("relevant_jobs")
                    print(len(relevant_jobs))
                    pj = Paginator(relevant_jobs, 5)
                    pjt = Paginator(relevant_jobs, 5)
                    pc = Paginator(common, 5)
                    pjs = Paginator(job_skills, 5)
                    pjq = Paginator(job_ques, 5)
                    pcp = Paginator(companyprofile, 5)
                    page_num = request.GET.get('page', 1)
                    try:
                        pj_objects = pj.page(page_num)
                        pjt_objects = pjt.page(page_num)
                        pc_objects = pc.page(page_num)
                        pjs_objects = pjs.page(page_num)
                        pjq_objects = pjq.page(page_num)
                        pcp_objects = pcp.page(page_num)
                    except EmptyPage:
                        pj_objects = pj.page(1)
                        pjt_objects = pjt.page(1)
                        pc_objects = pc.page(1)
                        pjs_objects = pjs.page(1)
                        pjq_objects = pjq.page(1)
                        pcp_objects = pcp.page(1)
                    objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                    return render(request, 'jobseeker/home.html',
                                  {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'pjs': pjt_objects})
                else:
                    u.first_login = True
                    u.save()
                    return redirect('jobseeker:create_profile')
            else:
                return redirect('/')
        else:
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
            return render(request, 'jobseeker/skills.html', {
                "user": u,
                "profile": profile,
                "address": address,
                "present_work": present_work,
                "past_work": past_work,
                "truck": truck,
                "driver": driver
            })


def ProfileEdit(request):
    try:
        profile = Candidate.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        profile = None
    print(profile)
    if profile is not None:
        if request.method == 'POST':
            form1 = ProfileRegisterForm(data=request.POST or None, files=request.FILES or None)
            form2 = ProfileRegisterForm_edu(request.POST or None)
            form3 = ProfileRegisterForm_profdetail(request.POST or None)
            form4 = ProfileRegisterForm_resume(request.POST or None)
            form5 = ProfileRegistration_skills(request.POST or None)
            form6 = ProfileRegistration_expdetail(request.POST or None)
            # print(form1)
            if form1.is_valid():
                print(form1.cleaned_data.get('profile_pic'))
                if form1.cleaned_data.get('birth_date'):
                    f1 = form1.save(commit=False)
                    try:
                        c = Candidate_profile.objects.get(user_id=profile)
                    except Candidate_profile.DoesNotExist:
                        c = None
                    if c:
                        c.delete()

                    f1.user_id = profile

                    f1.save()

            if form2.is_valid():
                f2 = form2.save(commit=False)
                if form2.cleaned_data.get('institute_name'):
                    f2.user_id = profile
                    f2.save()
            if form3.is_valid():
                f3 = form3.save(commit=False)
                if form3.cleaned_data.get('designation'):
                    f3.user_id = profile
                    f3.save()
            if form4.is_valid():
                if form4.cleaned_data.get('coverletter_text'):
                    f4 = form4.save(commit=False)
                    f4.user_id = profile
                    f4.save()

                # f5 = form5.save(commit=False)
                # f5.user_id = profile
                # f5.save()
            if form5.is_valid():
                if form5.cleaned_data.get('skill'):
                    f4 = form4.save(commit=False)
                    f4.user_id = profile
                    f4.save()
                # for form in form5:
                #     # extract name from each form and save
                #     skill = form.cleaned_data.get('skill')
                #     rating = form.cleaned_data.get('rating')
                #     # save book instance
                #     if skill:
                #         Candidate_skills(user_id=profile, skil=skill, rating=rating).save()
            if form6.is_valid():
                d = form6.cleaned_data.get('department')
                print(d)
                if d != "":
                    print("after d is not none")
                    try:
                        cep = Candidate_expdetail.objects.get(user_id=profile)
                    except Candidate_profile.DoesNotExist:
                        cep = None
                    if cep:
                        cep.delete()
                    f6 = form6.save(commit=False)
                    f6.user_id = profile
                    f6.save()
            return redirect('jobseeker:ProfileEdit')
        print(request.method)
        try:
            c = Candidate_profile.objects.get(user_id=profile)
            print(c)
        except Candidate_profile.DoesNotExist:
            c = None
            print(c)
        try:
            cr = Candidate_resume.objects.get(user_id=profile)
        except Candidate_resume.DoesNotExist:
            cr = None
        try:
            cep = Candidate_expdetail.objects.get(user_id=profile)
        except Candidate_expdetail.DoesNotExist:
            cep = None

        form1 = ProfileRegisterForm(instance=c)
        form2 = ProfileRegisterForm_edu()
        form3 = ProfileRegisterForm_profdetail()
        form4 = ProfileRegisterForm_resume(instance=cr)
        form5 = ProfileRegistration_skills()
        form6 = ProfileRegistration_expdetail(instance=cep)
        skills = Candidate_skills.objects.filter(user_id=profile)
        print(skills)
        edu = Candidate_edu.objects.filter(user_id=profile)
        professional = Candidate_profdetail.objects.filter(user_id=profile)
        return render(request, 'jobseeker/Profile.html',
                      {"form1": form1, 'form2': form2, "form3": form3, 'form4': form4, "form5": form5, 'form6': form6,
                       'skills': skills, 'edu': edu, 'professional': professional, 'c': c})

    else:
        return redirect('/')


def create_profile(request):
    profile = Candidate.objects.get(user=request.user)
    if request.method == 'POST':
        form1 = ProfileRegisterForm(request.POST)
        form2 = ProfileRegisterForm_edu(request.POST)
        form3 = ProfileRegisterForm_profdetail(request.POST)
        form4 = ProfileRegisterForm_resume(request.POST)
        form5 = ProfileRegistration_skills(request.POST)
        form6 = ProfileRegistration_expdetail(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid() and form6.is_valid():
            f1 = form1.save(commit=False)
            f1.user_id = profile
            f1.save()

            f2 = form2.save(commit=False)
            if f2.cleaned_data.get('institute_name'):
                f2.user_id = profile
                f2.save()

            f3 = form3.save(commit=False)
            if f2.cleaned_data.get('designation'):
                f3.user_id = profile
                f3.save()

            f4 = form4.save(commit=False)
            f4.user_id = profile
            f4.save()

            # f5 = form5.save(commit=False)
            # f5.user_id = profile
            # f5.save()
            for form in form5:
                # extract name from each form and save
                skill = form.cleaned_data.get('skill')
                rating = form.cleaned_data.get('rating')
                # save book instance
                if skill:
                    Candidate_skills(user_id=profile, skil=skill, rating=rating).save()

            f6 = form6.save(commit=False)
            f6.user_id = profile
            f6.save()
            return redirect('jobseeker:jobseeker_home')

    form1 = ProfileRegisterForm()
    form2 = ProfileRegisterForm_edu()
    form3 = ProfileRegisterForm_profdetail()
    form4 = ProfileRegisterForm_resume()
    form5 = ProfileRegistration_skills()
    form6 = ProfileRegistration_expdetail()

    return render(request, 'jobseeker/createprofile.html',
                  {"form1": form1, 'form2': form2, "form3": form3, 'form4': form4, "form5": form5, 'form6': form6})


def SavedJobs(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = shipJob.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
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
                    cp = Comp_profile.objects.get(user_id=c)
                except Comp_profile.DoesNotExist:
                    cp = None
                try:
                    cep = comp_PastWork.objects.get(user_id=c)
                except comp_PastWork.DoesNotExist:
                    cep = None

                if u.first_login:
                    print("len job")
                    print(len(job))
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
                        # print(diff)
                        if diff > 30:
                            # expired_job.append(j)
                            Expired_ShipJob.objects.create(job_id=j).save()

                        else:
                            jobs.append(j)
                        print("len")
                        print(len(jobs))
                    for jo in jobs:

                        e = jo.cust
                        companyprofile.append(Customer_profile.objects.get(comp=e))
                        try:
                            userS = shipJob_Saved.objects.get(job_id=jo.pk, comp=c)
                            # print(userS.job_id)
                        except shipJob_Saved.DoesNotExist:
                            userS = None
                        try:
                            userA = comp_Bids.objects.get(job_id=jo.pk, comp=c)
                            # print(userA.job_id)
                        except comp_Bids.DoesNotExist:
                            userA = None

                        if userA:
                            # print(userA)
                            continue
                        if userS:
                            # print(userS)
                            continue
                        relevant_jobs.append(jo)
                        print("job:")
                        print(jo)

                        job_ques.append(Shipment_Related_Question.objects.filter(job_id=jo))
                    print("job_quest:")
                    print(job_ques)
                    print("relevant_jobs")
                    print(len(relevant_jobs))
                    pj = Paginator(relevant_jobs, 5)
                    pjt = Paginator(relevant_jobs, 5)
                    pc = Paginator(common, 5)
                    pjs = Paginator(job_skills, 5)
                    pjq = Paginator(job_ques, 5)
                    pcp = Paginator(companyprofile, 5)
                    page_num = request.GET.get('page', 1)
                    try:
                        pj_objects = pj.page(page_num)
                        pjt_objects = pjt.page(page_num)
                        pc_objects = pc.page(page_num)
                        pjs_objects = pjs.page(page_num)
                        pjq_objects = pjq.page(page_num)
                        pcp_objects = pcp.page(page_num)
                    except EmptyPage:
                        pj_objects = pj.page(1)
                        pjt_objects = pjt.page(1)
                        pc_objects = pc.page(1)
                        pjs_objects = pjs.page(1)
                        pjq_objects = pjq.page(1)
                        pcp_objects = pcp.page(1)
                    objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                    return render(request, 'jobseeker/home.html',
                                  {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'pjs': pjt_objects})
                else:
                    u.first_login = True
                    u.save()
                    return redirect('jobseeker:create_profile')
            else:
                return redirect('/')


        else:

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

                    cp = Comp_profile.objects.get(user_id=c)

                except Comp_profile.DoesNotExist:

                    cp = None

                try:

                    cep = comp_PastWork.objects.get(user_id=c)

                except comp_PastWork.DoesNotExist:

                    cep = None

                if u.first_login:

                    job = shipJob.objects.all()

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

                        if diff > 30:

                            # expired_job.append(j)

                            Expired_ShipJob.objects.create(job_id=j).save()


                        else:

                            jobs.append(j)

                    for job in jobs:

                        e = job.cust

                        companyprofile.append(Customer_profile.objects.get(employer=e))

                        try:

                            userS = shipJob_Saved.objects.get(job_id=job.pk, candidate_id=c)

                            # print(userS.job_id)

                        except shipJob_Saved.DoesNotExist:

                            userS = None

                        try:

                            userA = comp_Bids.objects.get(job_id=job.pk, candidate_id=c)

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

                    pj = Paginator(relevant_jobs, 5)

                    pjt = Paginator(relevant_jobs, 5)

                    pc = Paginator(common, 5)

                    pjs = Paginator(job_skills, 5)

                    pjq = Paginator(job_ques, 5)

                    pcp = Paginator(companyprofile, 5)

                    page_num = request.GET.get('page', 1)

                    try:

                        pj_objects = pj.page(page_num)

                        pjt_objects = pjt.page(page_num)

                        pc_objects = pc.page(page_num)

                        pjs_objects = pjs.page(page_num)

                        pjq_objects = pjq.page(page_num)

                        pcp_objects = pcp.page(page_num)

                    except EmptyPage:

                        pj_objects = pj.page(1)

                        pjt_objects = pjt.page(1)

                        pc_objects = pc.page(1)

                        pjs_objects = pjs.page(1)

                        pjq_objects = pjq.page(1)

                        pcp_objects = pcp.page(1)

                    objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                    return render(request, 'jobseeker/home.html',

                                  {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'pjs': pjt_objects})


                else:

                    u.first_login = True

                    u.save()

                    return redirect('jobseeker:create_profile')

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


def AppliedJobs(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = shipJob.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
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
                    cp = Comp_profile.objects.get(user_id=c)
                except Comp_profile.DoesNotExist:
                    cp = None
                try:
                    cep = comp_PastWork.objects.get(user_id=c)
                except comp_PastWork.DoesNotExist:
                    cep = None

                if u.first_login:
                    print("len job")
                    print(len(job))
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
                        # print(diff)
                        if diff > 30:
                            # expired_job.append(j)
                            Expired_ShipJob.objects.create(job_id=j).save()

                        else:
                            jobs.append(j)
                        print("len")
                        print(len(jobs))
                    for jo in jobs:

                        e = jo.cust
                        companyprofile.append(Customer_profile.objects.get(comp=e))
                        try:
                            userS = shipJob_Saved.objects.get(job_id=jo.pk, comp=c)
                            # print(userS.job_id)
                        except shipJob_Saved.DoesNotExist:
                            userS = None
                        try:
                            userA = comp_Bids.objects.get(job_id=jo.pk, comp=c)
                            # print(userA.job_id)
                        except comp_Bids.DoesNotExist:
                            userA = None

                        if userA:
                            # print(userA)
                            continue
                        if userS:
                            # print(userS)
                            continue
                        relevant_jobs.append(jo)
                        print("job:")
                        print(jo)

                        job_ques.append(Shipment_Related_Question.objects.filter(job_id=jo))
                    print("job_quest:")
                    print(job_ques)
                    print("relevant_jobs")
                    print(len(relevant_jobs))
                    pj = Paginator(relevant_jobs, 5)
                    pjt = Paginator(relevant_jobs, 5)
                    pc = Paginator(common, 5)
                    pjs = Paginator(job_skills, 5)
                    pjq = Paginator(job_ques, 5)
                    pcp = Paginator(companyprofile, 5)
                    page_num = request.GET.get('page', 1)
                    try:
                        pj_objects = pj.page(page_num)
                        pjt_objects = pjt.page(page_num)
                        pc_objects = pc.page(page_num)
                        pjs_objects = pjs.page(page_num)
                        pjq_objects = pjq.page(page_num)
                        pcp_objects = pcp.page(page_num)
                    except EmptyPage:
                        pj_objects = pj.page(1)
                        pjt_objects = pjt.page(1)
                        pc_objects = pc.page(1)
                        pjs_objects = pjs.page(1)
                        pjq_objects = pjq.page(1)
                        pcp_objects = pcp.page(1)
                    objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                    return render(request, 'jobseeker/home.html',
                                  {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'pjs': pjt_objects})
                else:
                    u.first_login = True
                    u.save()
                    return redirect('jobseeker:create_profile')
            else:
                return redirect('/')
        else:
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
                    e = a.job_id.employer_id
                    companyprofile.append(Customer_profile.objects.get(employer=e))

                pj = Paginator(applied, 5)
                pjt = Paginator(applied, 5)
                pc = Paginator(companyprofile, 5)
                # pjs = Paginator(job_skills, 5)
                # pjq = Paginator(job_ques, 5)
                # pcp = Paginator(companyprofile, 5)
                page_num = request.GET.get('page', 1)
                try:
                    pj_objects = pj.page(page_num)
                    pjt_objects = pjt.page(page_num)
                    pc_objects = pc.page(page_num)
                    # pjs_objects = pjs.page(page_num)
                    # pjq_objects = pjq.page(page_num)
                    # pcp_objects = pcp.page(page_num)
                except EmptyPage:
                    pj_objects = pj.page(1)
                    pjt_objects = pjt.page(1)
                    pc_objects = pc.page(1)
                    # pjs_objects = pjs.page(1)
                    # pjq_objects = pjq.page(1)
                    # pcp_objects = pcp.page(1)
                objects = zip(pj_objects, pc_objects)

                return render(request, 'jobseeker/applied.html',
                              {'jobs': objects, 'c': c, 'cp': cp, 'pjs': pjt_objects})
                # objects = zip(applied, companyprofile)
                # return render(request, 'jobseeker/applied.html', {'jobs': objects, 'cp': cp})
            else:
                return redirect('/')


def remove_applied(request, pk):
    comp_Bids.objects.get(pk=pk).delete()

    return redirect('jobseeker:AppliedJobs')


def remove_saved(request, pk):
    c = patnerComp.objects.get(user=request.user)
    job = shipJob.objects.get(pk=pk)
    savej = shipJob_Saved.objects.filter(job_id=job)
    for s in savej:
        if s.candidate_id == c:
            s.delete()

    return redirect('jobseeker:SavedJobs')



