from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from morpheus.models import Survey, Question, Submission, Answer

class SubmissionAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')  # Log in the user
        
        # Create a survey and question
        self.survey = Survey.objects.create(title="Test Survey", description="Test description", created_by=self.user)
        self.question = Question.objects.create(survey=self.survey, text="What is your name?", question_type="text")
    
    def test_create_submission(self):
        data = {'survey': self.survey.id, 'answers': [{'question': self.question.id, 'response': 'John Doe'}]}
        response = self.client.post('/api/submissions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Submission.objects.count(), 1)

    def tearDown(self):
        # Clean up after the test to prevent issues with other tests
        User.objects.all().delete()
        Survey.objects.all().delete()
        Question.objects.all().delete()
        Submission.objects.all().delete()
        Answer.objects.all().delete()