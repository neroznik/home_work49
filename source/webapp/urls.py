"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path


from webapp.views.projects_views import ProjectsView, ProjectsCreateView, ProjectsUpdateView, ProjectsDeleteView, \
    IndexView
from webapp.views.tasks_views import TasksView, TasksCreateView, TasksUpdateView, TasksDeleteView
app_name = 'webapp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tasks/<int:pk>/', TasksView.as_view(), name='task_view'),
    path('project/<int:pk>/add_task/', TasksCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', TasksUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TasksDeleteView.as_view(), name ='task_delete'),
    path('project/<int:pk>/', ProjectsView.as_view(), name='project_view'),
    path('project/add/', ProjectsCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/update/', ProjectsUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectsDeleteView.as_view(), name='project_delete')

]
