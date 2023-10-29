from rest_framework import serializers
from .models import Question, Applicant, IQQuestion


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class IQQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IQQuestion
        fields = '__all__'

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'