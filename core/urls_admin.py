from django.urls import path, include
from . import views_admin
from django.contrib.auth import views as built_views

urlpatterns = [
    path('', views_admin.AdminAuth.as_view(), name='admin_auth'),
    path('control/', views_admin.ControlOperation.as_view(), name='control_operation'),
    path('testname/', views_admin.TestName.as_view(), name='Test_name'),
    path('seetest/', views_admin.ShowTestView.as_view(), name='See_Test'),
    path('deletetest/(?P<pk>\d+)', views_admin.DeleteTest.as_view(), name='Delete_Test'),
    path('edittest/', views_admin.EditTest.as_view(), name='Edit_Test'),
    path('toggle/(?P<pk>\d+)', views_admin.ToggleTestStatus.as_view(), name='toggle'),
    path('instructions/', views_admin.AdminInstructionView.as_view(), name='Instruction'),
    path('showinstructions/', views_admin.ShowInstructionView.as_view(), name='Show_Instruction'),
    path('deleteinstruction/(?P<pk>\d+)', views_admin.DeleteInstructionView.as_view(), name='Delete_Instruction'),
    path('editinstruction/(?P<pk>\d+)', views_admin.EditInstructionView.as_view(), name='Edit_Instruction'),
    path('deletealgorithm/(?P<pk>\d+)', views_admin.DeleteAlgorithmView.as_view(), name='Delete_Algorithm'),
    path('editalgorithm/(?P<pk>\d+)', views_admin.EditAlgorithmView.as_view(), name='Edit_Algorithm'),
    path('addquestion/', views_admin.AddQuestionView.as_view(), name='Add_Question'),
    path('addcategory/', views_admin.AddCategoryView.as_view(), name='Add_Category'),
    path('addalgorithm/', views_admin.AddAlgorithmView.as_view(), name='Add_Algorithm'),
    path('editcategory/', views_admin.Editcategory.as_view(), name='Edit_Category'),
    path('showquestions/', views_admin.ShowQuestionsView.as_view(), name='Show_Questions'),
    path('showcandidates/', views_admin.ShowCandidateListView.as_view(), name='Show_Candidates'),
    path('editquestion/(?P<pk>\d+)', views_admin.EditQuestionView.as_view(), name='Edit_Question'),
    path('deletequestion/(?P<pk>\d+)', views_admin.DeleteQuestionView.as_view(), name='Delete_Question'),
    path('deletecategory/(?P<pk>\d+)', views_admin.DeleteCategoryView.as_view(), name='Delete_Category'),
    path('viewresult/(?P<pk>\d+)', views_admin.ViewResultView.as_view(), name='View_result'),
    path('deleteresult/(?P<pk>\d+)', views_admin.DeleteResultView.as_view(), name='Delete_result'),
    path('logout/$', built_views.logout, {'next_page': 'admin_auth'}, name='logout'),

]
