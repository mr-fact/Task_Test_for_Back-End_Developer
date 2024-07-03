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
        responses=TaskInputSerializer(),
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
