from django.urls import include, path, reverse_lazy
from .views import SignUpView, ActivateAccount, login_candidate, customer_home, Add_Shipment, Add_prod_desc, unpublish, \
    remove_unpublish, job_detail, view_applied_candidate, shortlistview_applied_candidate, \
    disqualifyview_applied_candidate, shortlist, delete_job, disqualify, publish_job, ProfileView, job_Response, \
    SignUpVieww, Commission_View, Request_commision, select, Ship_ongoing,ProfileEdit
from django.contrib.auth import views as auth_views  # import this

app_name = 'customer'
urlpatterns = [
    path('login', login_candidate, name='customer/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/customer/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='customer/register'),
    path('signup/ref=<uid>', SignUpVieww.as_view(), name='ref'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html', email_template_name='account/password_reset_emailre.html',
        success_url=reverse_lazy('customer:password_reset_done')),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html",
        success_url=reverse_lazy('customer:password_reset_complete')), name='password_reset_confirm'),
    path('account/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('', customer_home, name='customer_home'),
    path('add_ship', Add_Shipment, name='job_post'),
    path('add_prod_desc/<int:pk>', Add_prod_desc, name='Add_prod_desc'),
    path('deletejob/<int:pk>', delete_job, name='delete_job'),
    path('jobdetail/<int:pk>', job_detail, name='job_detail'),
    path('jobdetail/publishjob/<int:pk>', publish_job, name='publish_job'),
    path('jobdetail/applied_candidate/<int:pk>', view_applied_candidate, name='view_applied_candidate'),
    path('jobdetail/applied_candidate/shortlistview/<int:pk>', shortlistview_applied_candidate,
         name='shortlist_view_applied_candidate'),
    path('jobdetail/applied_candidate/disqualifyview/<int:pk>', disqualifyview_applied_candidate,
         name='disqualify_view_applied_candidate'),
    path('jobdetail/applied_candidate/shortlist/<int:pk>', shortlist, name='shortlist'),
    path('jobdetail/applied_candidate/disqualify/<int:pk>', disqualify, name='disqualify'),
    path('jobdetail/applied_candidate/select/<int:pk>', select, name='select'),
    path('unpublish/<int:pk>', unpublish, name='unpublish'),
    path('removeunpublish/<int:pk>', remove_unpublish, name='remove_unpublish'),
    path('viewprofile/', ProfileView, name='profile'),
    path('profile_edit/', ProfileEdit, name='ProfileEdit'),
    path('create_profile/', ProfileEdit, name='create_profile'),
    path('account/', Commission_View, name='Commission'),
    path('account/request', Request_commision, name='Request_commision'),
    path('shipOnProgress/', Ship_ongoing, name='ShipOngoing')
]
