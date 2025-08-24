from . import views
from django.urls import path

urlpatterns = [
    path('', views.Loginview, name='login'),
    path('signup/', views.signupView, name='signup'),
    path('home/', views.homeView, name='home'),
    path('logout/', views.logoutView, name='logout'),
]
