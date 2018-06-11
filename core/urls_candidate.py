from django.urls import path
from . import views_candidate

urlpatterns = [
    path('signup/', views_candidate.CandidateRegistration.as_view(), name='signup'),
    path('', views_candidate.InstructionView.as_view(), name='home'),
    path('logout/', views_candidate.logout, name='session_out'),
    path('category/<category_name>/<int:id>', views_candidate.QuestionByCategory.as_view(), name='category'),
]
