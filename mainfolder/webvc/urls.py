from django.urls import path
from . import views

urlpatterns = [
    path('room/', views.room),
    path('', views.lobby),
]