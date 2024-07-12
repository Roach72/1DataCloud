from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='Login'),
    path('Logout/', views.logout_user, name='Logout'),
    path('Register/', views.register, name='Register'),


]

