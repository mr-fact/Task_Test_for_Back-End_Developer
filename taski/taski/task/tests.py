import datetime

from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from taski.project.models import Project
from taski.task.models import Task


class TaskTestCase(APITestCase):
    def setUp(self):
        cache.delete('all_tasks')
        self.project = Project(name='project1', description='description1')
        self.project.save()
        tasks = [
            Task(title=f'title{i}', description=f'description{i}', project=self.project, due_date='2024-07-05')
            for i
            in range(10000)
        ]
        Task.objects.bulk_create(tasks)
        self.url = '/api/tasks/'

    def test_cache(self):
        self.assertEqual(cache.get('all_tasks'), None)
        time_start = datetime.datetime.now()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        time_response1 = datetime.datetime.now()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        time_response2 = datetime.datetime.now()

        self.assertNotEquals(cache.get('all_tasks'), None)

        response = self.client.post(
            self.url,
            data={
                'title': 'title111',
                'description': 'description111',
                'project': self.project.id,
                'due_date': '2024-07-05'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cache.get('all_tasks'), None)

        # The response time with caching is less than half the response time without caching.
        self.assertTrue((time_response2-time_response1) < (time_response1-time_start) / 2)
