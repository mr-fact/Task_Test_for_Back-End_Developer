from rest_framework import status
from rest_framework.test import APITestCase

from taski.project.models import Project
from taski.project.serializers import ProjectSerializer


class ProjectTestCase(APITestCase):
    def setUp(self):
        self.project1 = Project(name='project1', description='description1')
        self.project1.save()
        self.project2 = Project(name='project2', description='description2')
        self.project2.save()
        self.project3 = Project(name='project3', description='description3')
        self.project3.save()

        self.url = '/api/projects/'

    def test_get_project_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            ProjectSerializer(Project.objects.all(), many=True).data
        )

    def test_create_project(self):
        response = self.client.post(self.url, data={'name': 'project4', 'description': 'description4'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.url, data={'name': 'project4', 'description': 'description4'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_project(self):
        response = self.client.put(
            self.url + '20000/',
            data={'name': 'project20000', 'description': 'description20000'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        first_project_id = Project.objects.first().id
        response = self.client.put(
            self.url + f'{first_project_id}/',
            data={'name': 'edited project', 'description': 'description'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(
            self.url + f'{first_project_id}/',
            data={'name': 'project2', 'description': 'description'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        first_project_id = Project.objects.first().id
        response = self.client.delete(self.url + f'{first_project_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(self.url + f'{first_project_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_project_detail(self):
        first_project = Project.objects.first()
        first_project_id = first_project.id
        response = self.client.get(self.url + f'{first_project_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProjectSerializer(first_project).data)
