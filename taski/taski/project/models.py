from django.db import models
from taski.common.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
