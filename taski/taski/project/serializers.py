from django.utils.text import slugify
from rest_framework import serializers

from taski.project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'slug',
            'name',
            'description',
        )

    def validate(self, attrs):
        if not self.instance and Project.objects.filter(slug=slugify(attrs.get('name'))).exists():
            raise serializers.ValidationError({'slug': 'this slug already exists'})
        return attrs
