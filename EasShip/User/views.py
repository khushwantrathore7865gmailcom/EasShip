from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from.models import User_custom
# Create your views here.
def loginUser(request):
    if request.user.is_authenticated and request.user.is_company:
        print(request.user)
        return redirect('partner_company:partner_company_home')
    elif request.user.is_authenticated and request.user.is_customer:
        print(request.user)
        return redirect('customer:customer_home')
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
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer:customer_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)