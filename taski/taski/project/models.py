from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from taski.common.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}'


@receiver(pre_save, sender=Project)
def add_slug_to_project(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
