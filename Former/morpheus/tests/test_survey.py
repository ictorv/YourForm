from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from morpheus.models import Survey
import warnings

class SurveyAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_create_survey(self):
        data = {'title': 'Test Survey', 'description': 'Survey description'}
        response = self.client.post('/api/surveys/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 1)

    def test_get_survey_list(self):
        Survey.objects.create(title='Test Survey 1', description='Description 1', created_by=self.user)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            response = self.client.get('/api/surveys/')    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_survey_details(self):
        survey = Survey.objects.create(title='Test Survey', description='Test description', created_by=self.user)
        response = self.client.get(f'/api/surveys/{survey.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], survey.title)

    def test_duplicate_survey(self):
        survey = Survey.objects.create(title='Original Survey', description='Test description', created_by=self.user)
        response = self.client.post(f'/api/surveys/{survey.id}/duplicate/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 2)
