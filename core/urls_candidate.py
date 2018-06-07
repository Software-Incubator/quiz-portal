from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.CandidateRegistration.as_view(), name='signup'),
    path('', views.Instruction.as_view(), name='home'),
    path('logout/', views.logout, name='session_out')
]
