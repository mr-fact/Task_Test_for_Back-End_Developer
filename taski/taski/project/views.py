from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet

from taski.project.models import Project
from taski.project.serializers import ProjectSerializer


@extend_schema_view(
    list=extend_schema(tags=['Project']),
    retrieve=extend_schema(tags=['Project']),
    create=extend_schema(tags=['Project']),
    update=extend_schema(tags=['Project']),
    partial_update=extend_schema(tags=['Project']),
    destroy=extend_schema(tags=['Project']),
)
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
