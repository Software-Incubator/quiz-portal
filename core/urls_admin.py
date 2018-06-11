from django.urls import path
from . import views_admin
from django.contrib.auth import views as built_views

urlpatterns = [
    path('', views_admin.AdminAuth.as_view(), name='admin_auth'),
    path('control/', views_admin.ControlOperation.as_view(), name='control_operation'),
    path('testname/', views_admin.TestName.as_view(), name='Test name'),
    path('instructions/', views_admin.AdminInstructionView.as_view(), name='Instruction'),
    path('addquestion/', views_admin.AddQuestionView.as_view(), name='Add Question'),
    path('addcategory/', views_admin.AddCategoryView.as_view(), name='Add Category'),
    path('Editcategory/', views_admin.Editcategory.as_view(), name='Edit Category'),
    path('showquestions/', views_admin.ShowQuestionsView.as_view(), name='Show Questions'),
    path('showcandidates/', views_admin.ShowCandidateListView.as_view(), name='Show Candidates'),
    path('editquestion/(?P<pk>\d+)', views_admin.EditQuestionView.as_view(), name='Edit Question'),
    path('deletequestion/(?P<pk>\d+)', views_admin.DeleteQuestionView.as_view(), name='Delete Question'),
    path('deletecategory/(?P<pk>\d+)', views_admin.DeleteCategoryView.as_view(), name='Delete Category'),
    path('viewresult/(?P<pk>\d+)', views_admin.ViewResultView.as_view(), name='View result'),
    path('logout/', built_views.logout, {'next_page': 'admin_auth'}, name='logout'),

]
