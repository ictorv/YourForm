from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from morpheus.models import Survey, Question, Answer, Submission

class AnalyticsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.survey = Survey.objects.create(title='Test Survey', description='Survey description', created_by=self.user)
        self.question = Question.objects.create(survey=self.survey, text='What is your name?', question_type='text')

    def test_get_analytics(self):
        submission = Submission.objects.create(survey=self.survey)
        Answer.objects.create(submission=submission, question=self.question, response='John Doe')
        response = self.client.get(f'/api/surveys/{self.survey.id}/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('analytics', response.data)
