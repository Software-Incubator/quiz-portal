from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AdminAuth.as_view(), name='admin_auth'),
    path('control/', views.ControlOperation.as_view(), name='control_operation'),
    path('testname/', views.TestName.as_view(), name='Test name'),
    path('instructions/', views.InstructionView.as_view(), name='Instruction'),
    path('addquestion/', views.AddQuestionView.as_view(), name='Add Question'),
    path('addcategory/', views.AddCategoryView.as_view(), name='Add Category'),
    path('editcategory/', views.editcategory.as_view(), name='comment'),

]
