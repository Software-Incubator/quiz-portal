from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.CandidateRegistration.as_view(), name='signup'),
    path('', views.InstructionView.as_view(), name='home'),
    path('logout/', views.logout, name='session_out'),
    path('start_test/', views.StartTest.as_view(), name='start_test'),
]
