from django.shortcuts import render
from pandas import unique
from .models import AudioFiles
from .serializers import AudioFilesSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.jwt import JWTAuthentication
from rest_framework.generics import ListAPIView

# Create your views here.


class selectedView(ListCreateAPIView):
    lookup_url_kwarg = "ChapterName"
    serializer_class = AudioFilesSerializer

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        queryset = AudioFiles.objects.filter(ChapterName=uid)
        return queryset


class idView(APIView):

    def get(self, request, id):
        queryset = AudioFiles.objects.get(id=id)
        serializer = AudioFilesSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, id):
        if (JWTAuthentication.authenticate(self, request)):
            queryset = AudioFiles.objects.get(id=id)
            serializer = AudioFilesSerializer(queryset, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Authentication Failed")


class AudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer

    def get_queryset(self):
        queryset = AudioFiles.objects.all()
        return queryset


class ApproveAudioFilesView(APIView):
    # authentication_classes = [JWTAuthentication]

    def post(self, request, audiofile_id):
        # if not JWTAuthentication.authenticate(self, request):
        #     return Response("Authentication Failed", status=status.HTTP_401_UNAUTHORIZED)
        print("here")
        try:
            audiofile = AudioFiles.objects.get(
                id=audiofile_id, is_approved=False)
        except AudioFiles.DoesNotExist:
            return Response("Audio file not found or already approved")

        # Approve the audio file
        audiofile.is_approved = True
        audiofile.save()

        serializer = AudioFilesSerializer(audiofile)
        return Response(serializer.data)


class ApprovedAudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer

    def get_queryset(self):
        queryset = AudioFiles.objects.filter(is_approved=True)
        return queryset


class NotApprovedAudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer

    def get_queryset(self):
        print("asdfg")
        queryset = AudioFiles.objects.filter(is_approved=False)
        return queryset
