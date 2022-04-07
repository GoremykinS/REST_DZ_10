from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate
from .views import ProjectModelViewSet
from .models import Project, Todo
# пользователя своего импортировать
from django.contrib.auth.models import User
from mixer.backend.django import mixer


class TestProjectApi(TestCase):

    def test_get_list(self):
        factory = APIRequestFactory()
        user = User.objects.create_superuser('serg', email='serg@mail.com', password='12345')
        request = factory.get('/api/projects')
        force_authenticate(request, user)
        view = ProjectModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_list_1(self):
        factory = APIRequestFactory()
        request = factory.get('/api/projects')
        view = ProjectModelViewSet.as_view({'get': 'list'})
        Project.objects.create(project_users='ivan ivanov', project_name='project_ivan', git_name='project_ivan.com')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_2(self):
        client = APIClient()
        response = client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_list_3(self):
        client = APIClient()
        Project.objects.create(project_users='ivan ivanov', project_name='project_ivan', git_name='project_ivan.com')
        response = client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class TestProjectClientApi(APITestCase):
    def setUp(self) -> None:
        self.project = mixer.blend(Project, git_name='project_ivan.com')

        self.admin = User.objects.create_superuser('serg', email='serg@mail.com', password='12345')

    def test_get_list(self):
        self.client.login(username='serg', password='12345')
        self.client.logout()
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_1(self):
        self.client.force_login(self.admin)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)