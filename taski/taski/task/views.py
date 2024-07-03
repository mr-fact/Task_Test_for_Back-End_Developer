from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from taski.task.models import Task
from taski.task.serialziers import TaskOutPutSerializer, TaskInputSerializer


class TaskAPIView(
    GenericAPIView,
):
    @extend_schema(
        tags=['task'],
        responses=TaskOutPutSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Task.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TaskOutPutSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TaskOutPutSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['task'],
        request=TaskInputSerializer(),
        responses=TaskOutPutSerializer(),
    )
    def post(self, request, *args, **kwargs):
        serializer = TaskInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
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
        responses=TaskOutPutSerializer(),
    )
    def get(self, request, id, *args, **kwargs):
        task = self.get_object()
        return Response(TaskOutPutSerializer(task).data)

    @extend_schema(
        tags=['task'],
        request=TaskInputSerializer(),
        responses=TaskOutPutSerializer(),
    )
    def put(self, request, id, *args, **kwargs):
        task = self.get_object()
        serializer = TaskInputSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TaskOutPutSerializer(task).data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['task'],
    )
    def delete(self, request, id, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
