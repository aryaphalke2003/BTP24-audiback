from pandas import unique

from authentication.jwt import JWTAuthentication
from .models import Quiz, Answer, Questions
from .serializers import *
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class QuizView(ListCreateAPIView):
    lookup_url_kwarg = "chapterName"
    serializer_class = QuizSerializer

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Quiz.objects.filter(chapterName=uid)
        return queryset


class QuestionsView(ListCreateAPIView):
    lookup_url_kwarg = "chapterName"
    serializer_class = AllQuestionsSerializer

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Questions.objects.filter(quiz__chapterName=uid)
        return queryset


class AnswersView(ListCreateAPIView):
    lookup_url_kwarg = "qid"
    serializer_class = AnswerSerializer

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Answer.objects.filter(question=uid)
        return queryset


# =============================================================================


class QuestionsIdView(APIView):
    def get(self, request, chapterName, id):
        queryset = Questions.objects.get(id=id, quiz__chapterName=chapterName)
        serializer = AllQuestionsSerializer(queryset)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, id, chapterName):
        if (JWTAuthentication.authenticate(self, request)):
            queryset = Questions.objects.get(
                id=id, quiz__chapterName=chapterName)
            serializer = AllQuestionsSerializer(queryset, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response("Authentication Failed")


class AnswersIdView(APIView):
    def get(self, request, qid, id, chapterName):
        queryset = Answer.objects.get(
            id=id, question__id=qid, question__quiz__chapterName=chapterName)
        serializer = AnswerSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, qid, id, chapterName):

        if (JWTAuthentication.authenticate(self, request)):
            queryset = Answer.objects.get(
                id=id, question__id=qid, question__quiz__chapterName=chapterName)
            serializer = AnswerSerializer(queryset, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response("Authentication Failed")


class AllQuizView(ListCreateAPIView):
    serializer_class = AllQuizSerializer

    def get_queryset(self):
        queryset = Quiz.objects.all()
        return queryset
