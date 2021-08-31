from django.urls import include, path
from .views import SignUpView, ActivateAccount, login_candidate, partner_company_home
from django.contrib.auth import views as auth_views  # import this

app_name = 'partner_company'
urlpatterns = [
    path('login', login_candidate, name='customer/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/customer/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='customer/register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('', partner_company_home, name='customer_home'),
    ]