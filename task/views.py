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

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)

    def created_tasks(self, request):
        user = request.user
        tasks = self.filter_queryset(self.get_queryset().filter(created_by=user))
        serializer = TasksListSerializer(tasks, many=True).data
        return Response(serializer)
    
    def assigned_tasks(self, request):
        user = request.user
        tasks = self.filter_queryset(self.get_queryset().filter(assigned_to=user))
        serializer = TasksListSerializer(tasks, many=True).data
        return Response(serializer)