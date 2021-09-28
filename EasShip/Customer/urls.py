from django.urls import include, path
from .views import SignUpView, ActivateAccount, login_candidate, customer_home, Add_Shipment, Add_prod_desc, unpublish, \
    remove_unpublish, job_detail, view_applied_candidate, shortlistview_applied_candidate, \
    disqualifyview_applied_candidate, shortlist, delete_job, disqualify, publish_job, ProfileView, job_Response
from django.contrib.auth import views as auth_views  # import this

app_name = 'customer'
urlpatterns = [
    path('login', login_candidate, name='customer/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/customer/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='customer/register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('', customer_home, name='customer_home'),
    path('add_ship', Add_Shipment, name='add_ship'),
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
    path('unpublish/<int:pk>', unpublish, name='unpublish'),
    path('removeunpublish/<int:pk>', remove_unpublish, name='remove_unpublish'),
    path('viewprofile/', ProfileView, name='profile'),
]
