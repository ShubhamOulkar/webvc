from django.urls import path
from . import views

urlpatterns = [
    path('room/', views.room),
    path('', views.lobby),
    path('get_token/', views.getToken),
    path('create_member/', views.createuser),
    path('get_member/', views.getmember),
]