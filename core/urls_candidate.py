from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('signup/', views.CandidateRegistration.as_view(), name='signup'),
    path('', views.InstructionView.as_view(), name='home'),
    path('logout/', views.logout, name='session_out'),
    path('start_test/',views.index, name = 'start_test'),
    # path('start_test/', views.StartTest.as_view(), name='start_test'),
    # path('question/<category>/', view=views.QuestionByCategory.as_view(), name='question'),
    # re_path( r'^(?P<category>\d+)$',view=views.QuestionByCategory.as_view(), name='question'),
    re_path(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),


]
