from django.urls import path, include

from taski.task.views import TaskAPIView

urlpatterns = [
    path('', TaskAPIView.as_view(), name='tasks',),
]
