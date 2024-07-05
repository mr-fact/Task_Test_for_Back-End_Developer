from rest_framework import serializers

from taski.project.models import Project
from taski.task.models import Task, Comment
from taski.task.services import add_new_comment_to_task


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


class TaskFieldSerializer(serializers.ModelSerializer):
    project = ProjectFieldSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class CommentOutPutSerializer(serializers.ModelSerializer):
    task = TaskFieldSerializer(read_only=True)

    class Meta:
        model = Comment
        depth = 1
        fields = (
            'author',
            'content',
            'task',
        )


class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'author',
            'content',
        )

    def validate(self, attrs):
        try:
            task = self.context.get('task')
            attrs['task'] = Task.objects.get(id=task)
        except Task.DoesNotExist:
            raise serializers.ValidationError({'task': 'task not found'})
        return attrs

    def create(self, validated_data):
        return add_new_comment_to_task(
            validated_data.get('author'),
            validated_data.get('content'),
            validated_data.get('task'),
        )
