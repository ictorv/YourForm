
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate question count
        if self.questions.count() >= Question.MAX_QUESTIONS:
            raise ValidationError(f"A survey cannot have more than {Question.MAX_QUESTIONS} questions.")

    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    MAX_QUESTIONS = 100
    
    QUESTION_TYPES = [
        ('text', 'Text Field'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
        # Future types (not implemented in MVP)
        ('ranking', 'Ranking'),
        ('linear_scale', 'Linear Scale'),
        ('date', 'Date Picker'),
        ('time', 'Time Picker'),
        ('file', 'File Upload'),
        ('matrix', 'Matrix/Grid'),
        ('image_choice', 'Image Choice'),
        ('slider', 'Slider'),
        ('signature', 'Signature'),
        ('color', 'Color Picker'),
        ('geolocation', 'Geolocation'),
        ('percentage', 'Percentage Allocation')
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=0)
    required = models.BooleanField(default=False)
    options = models.JSONField(null=True, blank=True)
    configuration = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['survey', 'order'],
                name='unique_question_order'
            )
        ]

    def clean(self):
        if self.question_type in ['dropdown', 'checkbox'] and not self.options:
            raise ValidationError("Options are required for dropdown and checkbox questions.")
        
        self.validate_configuration()

    def validate_configuration(self):
        """Validate configuration based on question type"""
        if self.question_type == 'linear_scale':
            config = self.configuration or {}
            if 'min' not in config or 'max' not in config:
                raise ValidationError("Linear scale questions require min and max values.")
            if config['min'] >= config['max']:
                raise ValidationError("Min value must be less than max value.")


class Submission(models.Model):
    survey = models.ForeignKey(Survey, related_name='submissions', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    submission = models.ForeignKey(Submission, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.JSONField()

class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title