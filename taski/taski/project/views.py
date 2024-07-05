from django.core.cache import cache
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from taski.project.models import Project
from taski.project.serializers import ProjectSerializer


@extend_schema_view(
    list=extend_schema(tags=['Project'], summary='List all projects'),
    retrieve=extend_schema(tags=['Project'], summary='Retrieve a single project by ID'),
    create=extend_schema(tags=['Project'], summary='Create a new project'),
    update=extend_schema(tags=['Project'], summary='Update a project by ID'),
    partial_update=extend_schema(tags=['Project'], summary='Update a project by ID'),
    destroy=extend_schema(tags=['Project'], summary='Delete a project by ID'),
)
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def list(self, request, *args, **kwargs):
        data = self.get_all_from_cache(request)
        if not data:
            data = self.get_all_from_db(request)
        return Response(data)

    def get_all_from_cache(self, request):
        data = cache.get(f'all_projects_{request.GET}')
        return data

    def get_all_from_db(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(f'all_projects_{str(request.GET)}', data, 600)  # 10 min / 600 sec
        return data

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            keys = cache.keys('all_projects_*')
            for key in keys:
                cache.delete(key)
        return response
