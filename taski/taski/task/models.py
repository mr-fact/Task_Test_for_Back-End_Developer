from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        event = 'created' if is_new else 'updated'
        self.send_notification(event)

    def delete(self, *args, **kwargs):
        self.send_notification('deleted')
        super().delete(*args, **kwargs)

    def send_notification(self, event):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "event": event,
                "task": {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "status": self.status,
                    "due_date": str(self.due_date),
                },
            },
        )

class Comment(BaseModel):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f'{self.id}-{self.task.title}'
