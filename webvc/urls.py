from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('login/', views.login_view, name='login_user'),
    path('logout/', views.logout_view, name='logout_user'),
    path('signup/', views.signup, name='signup_user'),
    path('room/', views.room),
    path('vcRoom/', views.hostVC, name='vcRoom'),
    path('get_token/', views.getToken),
    path('savechannel/', views.savechannel),
    path('join_member/', views.joinmember),
    path('send_email/',views.send_email, name='send_email'),
    path('verify_code/',views.verify_code, name='verify_code'),
    path('reset_password/', views.reset_password, name='reset_password'),
]