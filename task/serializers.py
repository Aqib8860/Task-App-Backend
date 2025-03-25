from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task



class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
    

class TasksListSerializer(TaskSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)
    assigned_to_details = serializers.SerializerMethodField(read_only=True)
    assigned_to = serializers.HiddenField(default=None)

    class Meta:
        model = Task
        fields = TaskSerializer.Meta.fields

    def get_created_by_name(self, task):
        if task.created_by:
            return f"{task.created_by.first_name}{task.created_by.last_name if task.created_by.last_name else ''}"

    def get_assigned_to_details(self, task):
        return task.assigned_to.values('id', 'first_name', 'last_name')