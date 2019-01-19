from django.urls import path, include
from . import views_admin
from django.contrib.auth import views as built_views

urlpatterns = [
    path('', views_admin.AdminAuth.as_view(), name='admin_auth'),
    path('control/', views_admin.ControlOperation.as_view(), name='control_operation'),
    path('testname/', views_admin.TestName.as_view(), name='Test_name'),
    path('seetest/', views_admin.ShowTestView.as_view(), name='See_Test'),
    path('deletetest/<int:pk>', views_admin.DeleteTest.as_view(), name='Delete_Test'),
    path('edittest/', views_admin.EditTest.as_view(), name='Edit_Test'),
    path('toggle/<int:pk>', views_admin.ToggleTestStatus.as_view(), name='toggle'),
    path('instructions/', views_admin.AdminInstructionView.as_view(), name='Instruction'),
    path('showinstructions/', views_admin.ShowInstructionView.as_view(), name='Show_Instruction'),
    path('deleteinstruction/<int:pk>', views_admin.DeleteInstructionView.as_view(), name='Delete_Instruction'),
    path('editinstruction/<int:pk>', views_admin.EditInstructionView.as_view(), name='Edit_Instruction'),
    path('addquestion/', views_admin.AddQuestionView.as_view(), name='Add_Question'),
    path('addcategory/', views_admin.AddCategoryView.as_view(), name='Add_Category'),
    path('editcategory/', views_admin.Editcategory.as_view(), name='Edit_Category'),
    path('showcategory/', views_admin.ShowCategoryView.as_view(), name='Show_Category'),
    path('showquestions/<int:pk>', views_admin.ShowQuestionsView.as_view(), name='Show_Questions'),
    path('showcandidates/', views_admin.ShowCandidateListView.as_view(), name='Show_Candidates'),
    path('editquestion/<int:pk>', views_admin.EditQuestionView.as_view(), name='Edit_Question'),
    path('deletequestion/<int:pk>', views_admin.DeleteQuestionView.as_view(), name='Delete_Question'),
    path('deletecategory/<int:pk>', views_admin.DeleteCategoryView.as_view(), name='Delete_Category'),
    path('viewresult/<int:pk>', views_admin.ViewResultView.as_view(), name='View_result'),
    path('deleteresult/<int:pk>', views_admin.DeleteResultView.as_view(), name='Delete_result'),
    path('logout', built_views.logout, {'next_page': 'admin_auth'}, name='logout'),
]
