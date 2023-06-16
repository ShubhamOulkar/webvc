from django.urls import path
from . import views

urlpatterns = [
    path('', views.start),
    path('login/', views.login, name='login_user'),
    path('signup/', views.signup, name='signup_user'),
    path('room/', views.room),
    path('get_token/', views.getToken),
    # path('create_member/', views.createuser),
    # path('get_member/', views.getmember),
]