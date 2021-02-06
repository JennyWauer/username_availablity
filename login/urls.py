from django.urls import path

from . import views

urlpatterns = [
    path('', views.login),
    path('register', views.register),
    path('user_login', views.user_login),
    path('log_off', views.log_off),    
    path('success', views.success),
    path('email', views.email),
]