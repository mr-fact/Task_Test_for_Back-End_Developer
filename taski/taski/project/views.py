from drf_spectacular.utils import extend_schema_view, extend_schema
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
