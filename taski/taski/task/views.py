from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from taski.api.serializers import NotFoundResponseSerializer, BadRequestResponseSerializer
from taski.task.models import Task, Comment
from taski.task.serialziers import TaskOutPutSerializer, TaskInputSerializer, CommentInputSerializer, \
    CommentOutPutSerializer


class TaskAPIView(
    GenericAPIView,
):
    @extend_schema(
        tags=['task'],
        summary='List all tasks',
        responses=TaskOutPutSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        data = self.get_all_from_cache()
        if not data:
            data = self.get_all_from_db()
        return Response(data)

    def get_all_from_cache(self):
        data = cache.get('all_tasks')
        return data

    def get_all_from_db(self):
        queryset = Task.objects.all()
        serializer = TaskOutPutSerializer(queryset, many=True)
        data = serializer.data
        cache.set('all_tasks', data, 600)  # 10 min / 600 sec
        return data

    @extend_schema(
        tags=['task'],
        summary='Create new task',
        request=TaskInputSerializer(),
        responses={
            200: TaskOutPutSerializer,
            400: BadRequestResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = TaskInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        cache.delete('all_tasks')
        return Response(TaskOutPutSerializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class SingleTaskAPIView(
    GenericAPIView,
):
    queryset = Task.objects.all()
    lookup_field = 'id'

    @extend_schema(
        tags=['task'],
        summary='Retrieve a single task by ID',
        responses={
            200: TaskOutPutSerializer,
            404: NotFoundResponseSerializer,
        },
    )
    def get(self, request, id, *args, **kwargs):
        task = self.get_object()
        return Response(TaskOutPutSerializer(task).data)

    @extend_schema(
        tags=['task'],
        summary='Update a task by ID',
        request=TaskInputSerializer(),
        responses={
            200: TaskOutPutSerializer,
            404: NotFoundResponseSerializer,
        },
    )
    def put(self, request, id, *args, **kwargs):
        task = self.get_object()
        serializer = TaskInputSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TaskOutPutSerializer(task).data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['task'],
        summary='Delete a task by ID',
        responses={
            204: None,
            404: NotFoundResponseSerializer,
        }
    )
    def delete(self, request, id, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentAPIView(
    APIView,
):
    @extend_schema(
        tags=['comment-task'],
        summary='Add a comment to a task',
        request=CommentInputSerializer(),
        responses={
            201: CommentOutPutSerializer,
            400: BadRequestResponseSerializer,
        },
    )
    def post(self, request, id, *args, **kwargs):
        serializer = CommentInputSerializer(data=request.data, context={'task': id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            CommentOutPutSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=['comment-task'],
        summary='List all comments for a task',
        responses={
            200: CommentOutPutSerializer,
        },
    )
    def get(self, request, id, *args, **kwargs):
        queryset = Comment.objects.filter(task__id=id)
        serializer = CommentOutPutSerializer(queryset, many=True)
        return Response(serializer.data)
