from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SurveyViewSet,
    QuestionViewSet,
    SubmissionViewSet,
    AnalyticsView,
    DuplicateSurveyView,
    AdminSurveysView,
    SaveFormAPIView,
    admin_dashboard,
    form_page,
    analytics_page,

)

router = DefaultRouter()
router.register(r'surveys', SurveyViewSet, basename='survey')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    # REST API endpoints
    path('', include(router.urls)),
    path('api/', include(router.urls)),
    path('surveys/<int:survey_id>/analytics/', AnalyticsView.as_view(), name='survey-analytics'),
    path('surveys/<int:survey_id>/duplicate/', DuplicateSurveyView.as_view(), name='survey-duplicate'),
    path('admin/surveys/', AdminSurveysView.as_view(), name='admin-surveys'),

    # Frontend render pages
    path('dashboard/', admin_dashboard, name='admin-dashboard'),
    path('form/<int:survey_id>/', form_page, name='form-page'),
    path('save-form/', SaveFormAPIView.as_view(), name='save-form'),
    path('analytics/<int:survey_id>/', analytics_page, name='analytics-page'),
]