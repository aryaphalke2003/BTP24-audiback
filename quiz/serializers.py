from rest_framework import serializers
from .models import Quiz,Questions,Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields="__all__"


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model=Questions
        fields="__all__"

class QuizSerializer(serializers.ModelSerializer):
    questions=QuestionsSerializer(many=True)
    class Meta:
        model=Quiz
        fields=['id','className','subjectName','chapterName',"questions"]

class AllQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields=['id','className','subjectName','chapterName']


class AllQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Questions
        fields=['text','quiz','id']