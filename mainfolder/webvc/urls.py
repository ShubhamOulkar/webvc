from django.urls import path
from . import views

urlpatterns = [
    path('', views.start),
    path('room/', views.room),
    path('lobby/', views.lobby),
    path('get_token/', views.getToken),
    path('create_member/', views.createuser),
    path('get_member/', views.getmember),
]