from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from collections import Counter
from .models import Survey, Question, Answer, Submission
from .serializers import SurveySerializer, QuestionSerializer, SubmissionSerializer, AnswerSerializer,FormSerializer

# Pagination class for larger datasets
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Survey ViewSet
class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = StandardResultsPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Validation helper for question data
def validate_question_data(data):
    if 'question_type' not in data:
        raise ValueError("Question type is required.")
    if data['question_type'] in ['checkbox', 'dropdown'] and not data.get('options'):
        raise ValueError("Questions of type 'checkbox' or 'dropdown' must include options.")

# Question ViewSet
class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            validate_question_data(data)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Submission ViewSet
class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        """
        Optionally filter submissions by the logged-in user or a specific survey
        """
        # Example: Filter by the current user (if submissions are user-related)
        user = self.request.user
        return Submission.objects.filter(survey__created_by=user)  # Filter submissions by the user's surveys
    
# Analytics View
class AnalyticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, survey_id):
        cache_key = f"analytics_{survey_id}"
        analytics = cache.get(cache_key)

        if not analytics:  # If not cached, compute analytics
            submissions = Submission.objects.filter(survey_id=survey_id)
            total_submissions = submissions.count()
            analytics = {}
            questions = Question.objects.filter(survey_id=survey_id)

            for question in questions:
                if question.question_type == 'text':
                    answers = Answer.objects.filter(question=question)
                    words = [word.lower() for answer in answers for word in answer.response.split() if len(word) >= 5]
                    word_count = Counter(words)
                    top_words = word_count.most_common(5)
                    others = sum([count for _, count in word_count.items() if _ not in dict(top_words)])
                    analytics[question.id] = {
                        'type': question.question_type,
                        'data': {
                            'top_words': [{'word': word, 'count': count} for word, count in top_words],
                            'others': others
                        }
                    }
                elif question.question_type in ['checkbox', 'dropdown']:
                    answers = Answer.objects.filter(question=question)
                    options = [tuple(answer.response) if question.question_type == 'checkbox' else answer.response for answer in answers]
                    option_count = Counter(options)
                    top_options = option_count.most_common(5)
                    others = sum([count for _, count in option_count.items() if _ not in dict(top_options)])
                    analytics[question.id] = {
                        'type': question.question_type,
                        'data': {
                            'top_options': [{'option': option, 'count': count} for option, count in top_options],
                            'others': others
                        }
                    }

            # Cache the analytics for 1 hour
            cache.set(cache_key, {"total_submissions": total_submissions, "analytics": analytics}, timeout=3600)

        # Return response with 'analytics' key at top level
        return Response({'analytics': analytics}, status=200)

# Duplicate Survey API
class DuplicateSurveyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, survey_id):
        try:
            survey = Survey.objects.get(id=survey_id, created_by=request.user)
            new_survey = Survey.objects.create(
                title=f"{survey.title} (Copy)",
                description=survey.description,
                created_by=request.user
            )
            for question in survey.questions.all():
                Question.objects.create(
                    survey=new_survey,
                    text=question.text,
                    question_type=question.question_type,
                    options=question.options,
                )
            return Response({"message": "Survey duplicated successfully!"}, status=201)
        except Survey.DoesNotExist:
            return Response({"detail": "Survey not found."}, status=404)

# Admin-specific surveys API
class AdminSurveysView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        surveys = Survey.objects.filter(created_by=request.user)
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=200)

class SaveFormAPIView(APIView):
    def post(self, request):
        form_data = request.data.get('form')
        questions_data = request.data.get('questions', [])

        # Serialize form data
        form_serializer = FormSerializer(data=form_data)
        if form_serializer.is_valid():
            form = form_serializer.save()

            # Now pass the form instance when creating questions
            for question_data in questions_data:
                question_data['form'] = form  # Associate each question with the form
                question_serializer = QuestionSerializer(data=question_data)
                if question_serializer.is_valid():
                    question_serializer.save()  # Save the question
                else:
                    return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'form': form_serializer.data,
                'questions': questions_data,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(form_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Render Admin Dashboard
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Render Form Page
def form_page(request, survey_id):
    return render(request, 'form_page.html', {'survey_id': survey_id})

# Render Analytics Page
def analytics_page(request, survey_id):
    return render(request, 'analytics_page.html', {'survey_id': survey_id})

from rest_framework.generics import ListAPIView
from .models import Survey
from .serializers import SurveySerializer

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all().order_by('created_at')  # Explicitly order by created_at or another field
    serializer_class = SurveySerializer

