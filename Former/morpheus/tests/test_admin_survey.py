from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from morpheus.models import Survey

class AdminSurveysAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_get_admin_surveys(self):
        Survey.objects.create(title='Test Survey 1', description='Description 1', created_by=self.user)
        response = self.client.get('/api/admin/surveys/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
