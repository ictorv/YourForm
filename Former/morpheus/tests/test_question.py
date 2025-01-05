from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from morpheus.models import Survey, Question

class QuestionAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.survey = Survey.objects.create(title='Test Survey', description='Survey description', created_by=self.user)

    def test_create_question(self):
        data = {'survey': self.survey.id, 'text': 'What is your name?', 'question_type': 'text'}
        response = self.client.post('/api/questions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_checkbox_question(self):
        data = {'survey': self.survey.id, 'text': 'Select your hobbies', 'question_type': 'checkbox', 'options': ['Reading', 'Traveling']}
        response = self.client.post('/api/questions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_question_list(self):
        Question.objects.create(survey=self.survey, text='What is your favorite color?', question_type='text')
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
