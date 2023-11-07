
from django.urls import path,include
from project_management import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('projectapi/',views.ProjectView),
    path('projectapi/<int:id>/',views.ProjectView),
    path('departmentapi/', views.DepartmentView.as_view()),
    path('departmentapi/<int:id>',views.DepartmentView.as_view()),
    path('documentapi/',views.DocumentView.as_view()),
    path('documentapi/<int:id>',views.Documentedit.as_view()),
    path('users/', views.UserView.as_view(), name='user-list'),
    path('users/<int:id>/', views.UserView.as_view(), name='user-detail'),
    path('files/', views.DocumentFilter.as_view(), name='File-details'),





]
