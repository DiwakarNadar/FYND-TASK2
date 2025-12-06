from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
