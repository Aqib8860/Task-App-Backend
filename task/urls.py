from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


router.register('task', views.TaskViewSet, basename='task')


urlpatterns = [
    path('', include(router.urls)),

    path('created-tasks', views.TaskViewSet.as_view({"get": "created_tasks"})),
    path('assigned-tasks', views.TaskViewSet.as_view({"get": "assigned_tasks"})),
    
    path('assign-task/<int:pk>/', views.TaskViewSet.as_view({"patch": "assign_task"})),
    path('unassign-task/<int:pk>/', views.TaskViewSet.as_view({"patch": "unassign_task"}))
]

