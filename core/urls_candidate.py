from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.CandidateRegistration.as_view(), name='signup'),

]