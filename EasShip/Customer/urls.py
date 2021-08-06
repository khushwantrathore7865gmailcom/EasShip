from django.urls import include, path
from .views import SignUpView, ActivateAccount, login_candidate, customer_home, Add_Shipment, Add_prod_desc
from django.contrib.auth import views as auth_views  # import this

app_name = 'customer'
urlpatterns = [
    path('login', login_candidate, name='customer/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/customer/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='customer/register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('', customer_home, name='customer_home'),
    path('add_ship', Add_Shipment, name='add_ship'),
    path('add_prod_desc/<int:pk>', Add_prod_desc, name='Add_prod_desc')
]
