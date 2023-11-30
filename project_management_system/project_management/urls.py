
from django.urls import path,include, re_path
from project_management import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('projectapi/',views.ProjectView),
    path('projectapi/<int:id>/',views.ProjectView),
    path('departmentapi/', views.DepartmentView.as_view()),
    path('departmentapi/<int:id>',views.DepartmentView.as_view()),
    path('documentapi/',views.DocumentView.as_view()),
    path('documentapi/<int:id>',views.Documentedit.as_view()),
    # path('users/', views.UserView.as_view(), name='user-list'),
    # path('users/<int:id>/', views.UserView.as_view(), name='user-detail'),
    # re_path('^files/$', views.DocumentFilter.as_view()),
    # re_path('^files/(?P<user_id>.+)/$', views.DocumentFilter.as_view()),
    re_path('^document/$', views.DepartmentFilter.as_view()),
    re_path('^document/(?P<department_id>.+)/$', views.DepartmentFilter.as_view()),
    path('', views.Userstats.as_view()),
    path('documentlist/', views.DocumentList.as_view()),
    path('projectlist/', views.ProjectList.as_view()),
    path('documentfilter/', views.Document.as_view()),
    path('project_count/', views.ProjectCount.as_view()),
    path('project_summary/', views.ProjectSummary.as_view()),
    path('summary/', views.Summary.as_view()),
    path('export/', views.ExportData.as_view()),
    # path('exports/', views.AlternativeExport.as_view()),
    path('count/', views.ProjectCountListApi.as_view())

]
