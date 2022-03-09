from django.urls import include, path, reverse_lazy
from .views import SignUpView, ActivateAccount, partner_company_Home, ProfileView, save_later, SavedJobs, AppliedJobs, \
    remove_applied, remove_saved, ProfileEdit, SignUpVieww, addTransport, addDriver, ManageDriver, ManageTruck, \
    Update_PresentShip, SetUp_PresentShip, PresentShip, DriverRecords, RemoveDriver, RemoveTruck, apply_Shipment, \
    TruckRecords,PastShipment,cancel_setup,Complete_PresentShip
from . import views
from django.contrib.auth import views as auth_views  # import this

app_name = 'partner_company'
urlpatterns = [
    path('', partner_company_Home, name='partner_company_home'),
    path('savedJobs/', SavedJobs, name='SavedJobs'),
    path('appliedJobs/', AppliedJobs, name='AppliedJobs'),
    path('PastShipment/', PastShipment, name='PastShipment'),
    path('removeApplied/<int:pk>', remove_applied, name='remove'),
    path('removeSaved/<int:pk>', remove_saved, name='remove_saved'),
    path('save/<int:pk>', save_later, name='save_job'),
    path('bid/<int:pk>', apply_Shipment, name='apply_Shipment'),
    path('login', views.login_candidate, name='partner_company/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup', SignUpView.as_view(), name='partner_company/register'),
    path('signup/ref=<uid>', SignUpVieww.as_view(), name='ref'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html', email_template_name='account/password_reset_email.html',
        success_url=reverse_lazy('partner_company:password_reset_done')),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html",
        success_url=reverse_lazy('partner_company:password_reset_complete')), name='password_reset_confirm'),
    path('account/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('viewprofile/', ProfileView, name='profile'),
    path('profile_edit/', ProfileEdit, name='ProfileEdit'),
    path('create_profile/', ProfileEdit, name='create_profile'),
    path('addTransport/', addTransport, name='add_transport'),
    path('addDriver/', addDriver, name='add_driver'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('ManageDriver/', ManageDriver, name='ManageDriver'),
    path('ManageTruck/', ManageTruck, name='ManageTruck'),
    path('Update_PresentShip/<int:pk>', Update_PresentShip, name='Update_PresentShip'),
    path('Complete_PresentShip/<int:pk>', Complete_PresentShip, name='Complete_PresentShip'),
    path('SetUp_PresentShip/<int:pk>', SetUp_PresentShip, name='SetUp_PresentShip'),
    path('cancel_SetUp/<int:pk>', cancel_setup, name='cancel_setup'),
    path('PresentShip/', PresentShip, name='PresentShip'),
    path('DriverRecords/', DriverRecords, name='DriverRecords'),
    path('VehicleRecords/', TruckRecords, name='VehicleRecords'),
    path('RemoveDriver/<int:pk>', RemoveDriver, name='RemoveDriver'),
    path('RemoveTruck/<int:pk>', RemoveTruck, name='RemoveTruck'),
]
