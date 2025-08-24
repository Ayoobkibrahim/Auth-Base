from . import views
from django.urls import path

urlpatterns =[
    path('',views.Loginview,name='login'),
    path('signup/',views.signupView,name='signup'),
]