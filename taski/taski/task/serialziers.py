from rest_framework import serializers

from taski.project.models import Project
from taski.task.models import Task


class ProjectFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class TaskOutPutSerializer(serializers.ModelSerializer):
    project = ProjectFieldSerializer(read_only=True)

    class Meta:
        model = Task
        depth = 1
        fields = (
            'id',
            'title',
            'description',
            'status',
            'due_date',
            'project',
        )


class TaskInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'status',
            'due_date',
            'project'
        )
