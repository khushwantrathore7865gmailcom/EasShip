from datetime import datetime
import json
import requests
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .utils import generate_id
import paytmchecksum
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from User.models import User_custom, Referral, Commission_request
from .forms import SignUpForm, ShipJob, prod_Detail_Formset, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from .tokens import account_activation_token
from .models import customer, Customer_profile, ProdDesc, shipJob, Expired_ShipJob, \
    Shipment_Related_Question
from PatnerCompany.models import shipJob_jobanswer, comp_Bids, Comp_address, Comp_profile, comp_Transport, \
    comp_PresentWork, comp_PastWork, comp_drivers

payment_id = "XiCkyY61890791146830"
payment_key = "PzkUpfSbO1sD5Be3"


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
    count = []
    sj = []
    cb = []
    c__p = []

    user = request.user
    context = {}

    if user is not None and user.is_customer:

        try:
            e = customer.objects.get(user=user)
        except customer.DoesNotExist:
            e = None
        # uncomment this after making the profile update correct
        # if Employer_profile.objects.get(employer=e):

        try:
            ep = Customer_profile.objects.get(cust=e)
        except Customer_profile.DoesNotExist:
            ep = None
        if user.first_login:
            job = shipJob.objects.filter(cust=e).exclude(bid_selected=True)
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

                if diff > 14:
                    Expired_ShipJob.objects.create(cust=j.cust, ship_title=j.ship_title,
                                                   job_description=j.job_description, picking_Address=j.picking_Address,
                                                   droping_Address=j.droping_Address).save()

                    j.delete()

                else:
                    jobs.append(j)
                    c_b = comp_Bids.objects.filter(job_id=j)

                    if c_b is None:
                        count.append(0)
                    else:
                        count.append(c_b.count())
                expired_job = Expired_ShipJob.objects.filter(cust=e)
                o = zip(jobs, count)
                sjob = shipJob.objects.filter(cust=e, bid_selected=True)
                pay = False
                for s in sjob:
                    p = comp_PresentWork.objects.get(job_id=s)
                    sj.append(p)

                    if p.payment_Done == "":
                        pay = True
                    cbid = Comp_profile.objects.get(comp=p.comp)
                    print(cbid)
                    cb.append(cbid)

                object = zip(sj, cb)
                context = {'jobs': o, 'expired': expired_job, 'og': object, 'ep': ep, 'pay': pay}

            return render(request, 'customer/job-post.html', context)
        else:
            user.first_login = True
            user.save()
            return redirect('customer:create_profile')
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
        try:
            cp = Customer_profile.objects.get(cust=users)
        except Customer_profile.DoesNotExist:
            cp = None
        form = ShipJob()
        if request.method == 'POST':
            form = ShipJob(request.POST)
            f = form.save(commit=False)
            f.cust = users

            f.save()
            pk = f.pk
            print(pk)
            return redirect('customer:Add_prod_desc', pk)
        return render(request, 'customer/addjob.html', {'form': form, 'ep': cp})
    else:
        return redirect('/')


def unpublish(request, pk):
    user = request.user
    j = shipJob.objects.get(pk=pk)
    # print(c)
    # print(job)
    Expired_ShipJob.objects.create(cust=j.cust, ship_title=j.ship_title,
                                   job_description=j.job_description, picking_Address=j.picking_Address,
                                   droping_Address=j.droping_Address).save()

    j.delete()
    return redirect('recruiter:employer_home')


def remove_unpublish(request, pk):
    j = Expired_ShipJob.objects.get(pk=pk)
    shipJob.objects.create(cust=j.cust, ship_title=j.ship_title,
                           job_description=j.job_description, picking_Address=j.picking_Address,
                           droping_Address=j.droping_Address).save()
    j.delete()

    return redirect('recruiter:employer_home')


def Add_prod_desc(request, pk):
    u = request.user

    users = customer.objects.get(user=u)
    try:
        cp = Customer_profile.objects.get(cust=users)
    except Customer_profile.DoesNotExist:
        cp = None
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

    return render(request, 'customer/add_job_desc.html', {"form2": form, 'ep': cp})


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


def Bid_detail(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        e = customer.objects.get(user=request.user)
        job = comp_Bids.objects.get(pk=pk)
        company = Comp_profile.objects.get(comp=job.comp)
        # candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
        # objects = zip(job,candidate_Applied)
        return render(request, 'customer/Bid_details.html', {'job': job, 'c': company})
    else:
        return redirect('/')


@login_required(login_url='/')
def view_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        candidate_user = []
        candidate_profile = []

        candidate_answer = []

        rating = []
        number = []
        e = customer.objects.get(user=request.user)

        cp = Customer_profile.objects.get(cust=e)
        job = shipJob.objects.get(pk=pk)

        question = Shipment_Related_Question.objects.filter(job_id=job)
        candidate_Applied = comp_Bids.objects.filter(job_id=job)
        for can in candidate_Applied:

            c = can.comp
            try:
                c_p = Comp_profile.objects.get(comp=c)
            except Comp_profile.DoesNotExist:
                c_p = None

            try:
                p_p = comp_PastWork.objects.filter(comp=c)
            except comp_PastWork.DoesNotExist:
                p_p = None
            count = len(p_p)
            number.append(count)
            r = 0
            for p in p_p:
                r = r + p.Rating
            if count == 0:
                rating.append(0)
            else:
                rating.append(r / count)
            candidate_profile.append(c_p)
            print("working filter")
            print(candidate_profile)
            candidate_user.append(c.user)

            for q in question:
                candidate_answer.append(
                    shipJob_jobanswer.objects.get(question_id=q, candidate_id=c))

        quest = zip(question, candidate_answer)
        # print(candidate_answer)
        objects = zip(candidate_profile, candidate_user, candidate_Applied, number, rating)

        return render(request, 'customer/job_candidate.html',
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
        cp = Customer_profile.objects.get(cust=e)
        candidate_user = []
        candidate_profile = []
        address_profile = []
        professional_profile = []
        c_bid = []
        candidate_answer = []

        job = shipJob.objects.get(pk=pk)
        question = Shipment_Related_Question.objects.filter(job_id=job)
        candidate_Applied = comp_Bids.objects.filter(job_id=job)
        for can in candidate_Applied:
            c = can.candidate_id
            c_bid.append(c)
            candidate_profile.append(Comp_profile.objects.get(comp=c))
            candidate_user.append(c.user)
            address_profile.append(Comp_address.objects.filter(comp=c))
            professional_profile.append(comp_PastWork.objects.filter(comp=c))

            for q in question:
                candidate_answer.append(shipJob_jobanswer.objects.get(question_id=q, candidate_id=c))

        objects = zip(candidate_profile, address_profile, professional_profile,
                      candidate_user, candidate_Applied, c_bid)
        # question = zip(question, candidate_answer)
        return render(request, 'customer/shortlisted_view.html',
                      {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer, 'cp': cp})
    else:
        return redirect('/')


@login_required(login_url='/')
def disqualifyview_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_customer:
        e = customer.objects.get(user=user)
        cp = Customer_profile.objects.get(cust=e)
        candidate_user = []
        candidate_profile = []
        address_profile = []
        professional_profile = []

        candidate_answer = []

        job = shipJob.objects.get(pk=pk)
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
        return render(request, 'customer/disqualified.html',
                      {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer, 'cp': cp})
    else:
        return redirect('/')


@login_required(login_url='/')
def shortlist(request, pk):
    e = comp_Bids.objects.get(pk=pk)
    e.is_shortlisted = True
    e.is_selected = False
    e.is_disqualified = False
    e.save()
    print(e.job_id.pk)
    return redirect('customer:view_applied_candidate', e.job_id.pk)


@login_required(login_url='/')
def select(request, pk):
    user = request.user
    e = comp_Bids.objects.get(pk=pk)
    e.is_shortlisted = False
    e.is_disqualified = False
    e.is_selected = True
    e.save()
    pks = e.job_id.pk
    s = shipJob.objects.get(pk=pks)
    s.bid_selected = True
    s.save()
    cb = comp_Bids.objects.filter(job_id=s)
    for c in cb:
        if c.is_selected:
            try:
                r = Referral.objects.get(user=user)
            except Referral.DoesNotExist:
                r = None
            if r:
                r.commissions = e.Bid_amount * 0.05
                r.save()

    return redirect('customer:view_applied_candidate', e.job_id.pk)


@login_required(login_url='/')
def disqualify(request, pk):
    e = comp_Bids.objects.get(pk=pk)
    e.is_shortlisted = False
    e.is_disqualified = True
    e.is_selected = False
    e.save()
    print(e.job_id.pk)
    return redirect('customer:view_applied_candidate', e.job_id.pk)


@login_required(login_url='/')
def delete_job(request, pk):
    ShipJob.objects.get(pk=pk).delete()

    return redirect('customer:customer_home')


@login_required(login_url='/')
def publish_job(request, pk):
    e = ShipJob.objects.get(pk=pk)
    e.is_save_later = False
    e.save()
    return redirect('customer:job_detail', pk)


@login_required(login_url='/')
def ProfileView(request):
    oldshipment = []
    u = request.user
    e = customer.objects.get(user=u)
    try:
        profile = Customer_profile.objects.get(cust=e)
    except Customer_profile.DoesNotExist:
        profile = None
    sp = shipJob.objects.filter(cust=e)
    for s in sp:
        if s.is_completed:
            oldshipment.append(comp_PastWork.objects.get(jobid=s))

    return render(request, 'customer/skills.html', {
        "user": u,
        "profile": profile,
        "past_work": oldshipment
    })


def ProfileEdit(request):
    user = request.user
    c = customer.objects.get(user=request.user)
    if c is not None:
        try:
            cp = Customer_profile.objects.get(cust=c)
        except Customer_profile.DoesNotExist:
            cp = None
        if cp is None:
            if request.method == 'POST':
                form = Profile(request.POST or None, request.FILES or None)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.cust = c
                    f.save()
            form = Profile()
        else:
            if request.method == "POST":
                form = Profile(request.POST, request.FILES, instance=cp)
                if form.is_valid():
                    form.save()

                    return redirect('customer:profile')

            form = Profile(instance=cp)
        return render(request, 'partner_company/EditProfile.html', {'form': form})
    else:
        return redirect('/')


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
            if r.commission_status == "not done":
                total = total + r.commissions
                r.commission_status = "request sent"
                r.save()
            if r.commission_status == "request sent":
                total = total + r.commissions
                messages = "request is sent payment will be done in 5-7 working days "

        return render(request, 'customer/Commission_view.html', {'com': total, 'referred': re, 'message': messages})
    else:
        return redirect('/')


def Ship_ongoing(request):
    user = request.user
    sj = []
    cb = []
    if user is not None and user.is_customer:
        sjob = shipJob.objects.filter(cust=user, bid_selected=True)
        for s in sjob:
            sj.append(s)
            cbid = comp_Bids.objects.filter(job_id=s)
            cb.append(cbid)
        object = zip(sj, cb)
        return render(request, 'customer/ship_ongoing.html', {'obj': object})
    else:
        return redirect('/')


def payPayment(request, pk):
    c_pwork = comp_PresentWork.objects.get(pk=pk)
    company = Comp_profile.objects.get(comp=c_pwork.comp)
    if request.method == 'POST':

        if c_pwork.payment_Done:
            pay = c_pwork.Total_payment.Bid_amount - c_pwork.payment_Done
        else:
            pay = (c_pwork.Total_payment.Bid_amount) / 2

        order_id = generate_id()
        paytmParams = dict()
        paytmParams["body"] = {
            "requestType": "Payment",
            "mid": payment_id,
            "websiteName": "WEBSTAGING",
            "orderId": order_id,
            "callbackUrl": reverse('customer:customer_home'),
            "txnAmount": {
                "value": str(pay),
                "currency": "INR",
            },
            "userInfo": {
                "custId": c_pwork.job_id.cust.user.email,
            },
        }
        checksum = paytmchecksum.PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), payment_key)
        paytmParams["head"] = {
            "signature": checksum
        }

        post_data = json.dumps(paytmParams)
        url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={payment_id}&orderId={order_id}"

        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
        print(response)
        payment_page = {
            'mid': payment_id,
            'txnToken': response['body']['txnToken'],
            'orderId': paytmParams['body']['orderId'],
        }
        return render(request, 'customer/paytm.html', {'data': payment_page})
    return render(request, 'customer/checkout.html', {'cp': c_pwork, 'c': company})


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    param_dict = {}
    order_id = request.POST.get('ORDERID')
    payment_mode = request.POST.get('PAYMENTMODE')
    transaction_id = request.POST.get('TXNID')
    Bank_transaction_id = request.POST.get('BANKTXNID')
    # transaction_id = request.POST.get('TXNDATE')
    res_msg = request.POST.get('RESPMSG')
    for i in form.keys():
        param_dict[i] = form[i]

    checksum = request.POST.get('CHECKSUMHASH')
    verify = paytmchecksum.PaytmChecksum.verifySignature(param_dict, payment_key, checksum)
    if verify:
        if param_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + param_dict['RESPMSG'])
    return render(request, 'customer/paymentstatus.html', {'response': param_dict})
