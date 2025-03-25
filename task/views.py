from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .serializers import TaskSerializer, TasksListSerializer
from.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'assigned_to': ['exact'],
        'status': ['exact'], 
        'task_type': ['exact'], 
        'created_at': ['date'],
    }
    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(assigned_to=user) | Q(created_by=user)).distinct()

    # Create A New Task
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)

    # Assign a task to multiple users.
    def assign_task(self, request, pk=None):
        task = Task.objects.filter(id=pk).first()
        if not task:
            return Response({"msg": "Task not found."}, status=404)
        
        assigned_users = request.data.get('assigned_to', [])
        
        if not isinstance(assigned_users, list):
            return Response({"msg": "assigned_to must be a list of user IDs."}, status=400)
        
        task.assigned_to.add(*assigned_users)  # Assign users to task
        task.save()
        return Response({"msg": "Task assigned successfully!"}, status=200)
        
    # UNAssign a task to multiple users.
    def unassign_task(self, request, pk=None):
        task = Task.objects.filter(id=pk).first()
        if not task:
            return Response({"msg": "Task not found."}, status=404)
        
        assigned_users = request.data.get('assigned_to', [])
        
        if not isinstance(assigned_users, list):
            return Response({"msg": "assigned_to must be a list of user IDs."}, status=400)
        
        task.assigned_to.remove(*assigned_users)  # Assign users to task
        task.save()
        return Response({"msg": "Task Unassigned successfully!"}, status=200)
        
    # Get User Create Tasks
    def created_tasks(self, request):
        user = request.user
        tasks = self.filter_queryset(self.get_queryset().filter(created_by=user))
        serializer = TasksListSerializer(tasks, many=True).data
        return Response(serializer)
    
    # Get User Assigned tasks
    def assigned_tasks(self, request):
        user = request.user
        tasks = self.filter_queryset(self.get_queryset().filter(assigned_to=user))
        serializer = TasksListSerializer(tasks, many=True).data
        return Response(serializer)