from django.urls import path

from taski.task.views import TaskAPIView, SingleTaskAPIView

urlpatterns = [
    path('', TaskAPIView.as_view(), name='tasks',),
    path('<int:id>/', SingleTaskAPIView.as_view(), name='single-tasks',),
]
