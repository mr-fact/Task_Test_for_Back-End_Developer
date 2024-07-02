from django.db import models
from taski.common.models import BaseModel
from taski.project.models import Project


class Task(BaseModel):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'InProgress'),
            ('completed', 'Completed')
        ],
        default='pending'
    )
    due_date = models.DateField()

    def __str__(self):
        return f'{self.id}-{self.title}'


class Comment(BaseModel):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f'{self.id}-{self.task.title}'
