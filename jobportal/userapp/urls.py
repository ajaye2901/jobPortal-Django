from django.urls import path
from userapp.views import *


urlpatterns = [
    path('register_company/', register_company, name='register_company'),
    path('login_company/',login_company, name='login_company'), 
    path('user_register/', user_register, name='user_register'),
    path('user_login/',user_login, name='user_login'),

    path('mainlogin/',mainlogin,name='mainlogin'), 
]