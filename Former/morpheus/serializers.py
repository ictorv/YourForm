from rest_framework import serializers
from .models import Survey, Question, Answer, Submission,Form


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'survey', 'text', 'question_type', 'order', 'required', 'options', 'configuration']

    def validate(self, data):
        survey = data.get('survey')
        if survey and survey.questions.count() >= Question.MAX_QUESTIONS:
            raise serializers.ValidationError(
                f"This survey already has the maximum number of questions ({Question.MAX_QUESTIONS})"
            )
        return data

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'response']

class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'submitted_at', 'survey', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        submission = Submission.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(submission=submission, **answer_data)
        return submission

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Form
        fields = ['title', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        form = Form.objects.create(**validated_data)

        for question_data in questions_data:
            Question.objects.create(form=form, **question_data)

        return form


