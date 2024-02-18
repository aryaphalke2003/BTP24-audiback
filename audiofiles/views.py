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
        queryset = AudioFiles.objects.filter(ChapterName=uid, is_approved=True)
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
    
    
class AddAudioFilesView(ListCreateAPIView):
    serializer_class=AudioFilesSerializer
    
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES['audio_file']
        print(audio_file);
          # Check if the audio file exists in the request
        if not audio_file:
            return Response({'error': 'No audio file provided'}, status=400)

        # Create a new AudioFiles object with the uploaded file
        audio_file_instance = AudioFiles.objects.create(
            AudioFile=audio_file,
            # Add other fields if necessary
        )

        # Serialize the newly created object
        serializer = AudioFilesSerializer(audio_file_instance)
        # You can handle the uploaded file here, for example, save it to a specific directory or process it in any way you need.
        # You can also create an AudioFiles object and save it to the database.
        return Response({'status': 'File uploaded successfully'}, status=200)
