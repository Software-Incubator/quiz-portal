from django.urls import path, include, re_path
from . import views_admin
from django.contrib.auth import views as built_views

urlpatterns = [
    re_path('', views_admin.AdminAuth.as_view(), name='admin_auth'),
    re_path('control/', views_admin.ControlOperation.as_view(), name='control_operation'),
    re_path('testname/', views_admin.TestName.as_view(), name='Test_name'),
    re_path('seetest/', views_admin.ShowTestView.as_view(), name='See_Test'),
    re_path('deletetest/(?P<pk>\d+)', views_admin.DeleteTest.as_view(), name='Delete_Test'),
    re_path('edittest/', views_admin.EditTest.as_view(), name='Edit_Test'),
    re_path('toggle/(?P<pk>\d+)', views_admin.ToggleTestStatus.as_view(), name='toggle'),
    re_path('instructions/', views_admin.AdminInstructionView.as_view(), name='Instruction'),
    re_path('showinstructions/', views_admin.ShowInstructionView.as_view(), name='Show_Instruction'),
    re_path('deleteinstruction/(?P<pk>\d+)', views_admin.DeleteInstructionView.as_view(), name='Delete_Instruction'),
    re_path('editinstruction/(?P<pk>\d+)', views_admin.EditInstructionView.as_view(), name='Edit_Instruction'),
    re_path('deletealgorithm/(?P<pk>\d+)', views_admin.DeleteAlgorithmView.as_view(), name='Delete_Algorithm'),
    re_path('editalgorithm/(?P<pk>\d+)', views_admin.EditAlgorithmView.as_view(), name='Edit_Algorithm'),
    re_path('addquestion/', views_admin.AddQuestionView.as_view(), name='Add_Question'),
    re_path('addcategory/', views_admin.AddCategoryView.as_view(), name='Add_Category'),
    re_path('addalgorithm/', views_admin.AddAlgorithmView.as_view(), name='Add_Algorithm'),
    re_path('editcategory/', views_admin.Editcategory.as_view(), name='Edit_Category'),
    re_path('showcategory/', views_admin.ShowCategoryView.as_view(), name='Show_Category'),
    re_path('showquestions/(?P<pk>\d+)', views_admin.ShowQuestionsView.as_view(), name='Show_Questions'),
    re_path('showcandidates/', views_admin.ShowCandidateListView.as_view(), name='Show_Candidates'),
    re_path('editquestion/(?P<pk>\d+)', views_admin.EditQuestionView.as_view(), name='Edit_Question'),
    re_path('deletequestion/(?P<pk>\d+)', views_admin.DeleteQuestionView.as_view(), name='Delete_Question'),
    re_path('deletecategory/(?P<pk>\d+)', views_admin.DeleteCategoryView.as_view(), name='Delete_Category'),
    re_path('viewresult/(?P<pk>\d+)', views_admin.ViewResultView.as_view(), name='View_result'),
    re_path('deleteresult/(?P<pk>\d+)', views_admin.DeleteResultView.as_view(), name='Delete_result'),
    re_path('logout/$', built_views.logout, {'next_page': 'admin_auth'}, name='logout'),
]
