from django.urls import path
from . import views_candidate

urlpatterns = [
    # path('', views_candidate.GetTestView.as_view(), name='get_test'),
    path('', views_candidate.CandidateRegistration.as_view(), name='signup'),
    path('instruction/', views_candidate.InstructionView.as_view(), name='instruction'),
    path('logout/', views_candidate.logout, name='session_out'),
    path('category/<category_name>/<int:id>', views_candidate.QuestionByCategory.as_view(), name='category'),
    # path('answer/', views_candidate.UserAnswerView.as_view(), name="answer"),
    path('user_answer/', views_candidate.DefaultOption.as_view(), name="user_answer"),
    path('save_status/', views_candidate.SaveStatus.as_view(), name="save_status")
]
