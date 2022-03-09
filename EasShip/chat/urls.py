from django.urls import include, path, reverse_lazy
from .views import room,send,getMessages
from django.contrib.auth import views as auth_views  # import this

app_name = 'chat'
urlpatterns = [
    path('<str:room>/',room,name ='room'),
    path('send', send, name='send'),
    path('getMessages/<str:room>/', getMessages, name='getMessages'),
]
