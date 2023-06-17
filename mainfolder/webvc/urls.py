from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('login/', views.login_view, name='login_user'),
    path('logout/', views.logout_view, name='logout_user'),
    path('signup/', views.signup, name='signup_user'),
    path('room/', views.room),
    path('lobby/', views.lobby, name='lobby'),
    path('get_token/', views.getToken),
    # path('create_member/', views.createuser),
    # path('get_member/', views.getmember),
]