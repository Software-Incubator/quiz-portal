from django.urls import path, include
from . import views
from django.contrib.auth import views as built_views

urlpatterns = [
    path('', views.AdminAuth.as_view(), name='admin_auth'),
    path('control/', views.ControlOperation.as_view(), name='control_operation'),
    path('testname/', views.TestName.as_view(), name='Test name'),
    path('instructions/', views.InstructionView.as_view(), name='Instruction'),
    path('addquestion/', views.AddQuestionView.as_view(), name='Add Question'),
    path('addcategory/', views.AddCategoryView.as_view(), name='Add Category'),
    path('editcategory/', views.editcategory.as_view(), name='Edit Category'),
    path('showquestions/', views.ShowQuestionsView.as_view(), name='Show Questions'),
    path('editquestion/(?P<pk>\d+)', views.EditQuestionView.as_view(), name='Edit Question'),
    path('deletequestion/(?P<pk>\d+)', views.DeleteQuestionView.as_view(), name='Delete Question'),
    path('deletecategory/(?P<pk>\d+)', views.DeleteCategoryView.as_view(), name='Delete Category'),
    path('logout/$', built_views.logout, {'next_page': 'admin_auth'}, name='logout'),

]
