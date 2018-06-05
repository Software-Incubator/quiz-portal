from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AdminAuth.as_view(), name='admin_auth'),
    path('control/', views.ControlOperation.as_view(), name='control_operation'),

]