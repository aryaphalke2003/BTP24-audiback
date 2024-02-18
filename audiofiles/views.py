from django.shortcuts import render
from pandas import unique
from .models import AudioFiles
from .serializers import AudioFilesSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.jwt import JWTAuthentication
from rest_framework.generics import ListAPIView
# from .models import Grade, Subject, Chapter
from .serializers import GradeSerializer, SubjectSerializer, ChapterSerializer, ChaptersSerializer
from rest_framework import status
from .models import Grade, Subject, Chapter, Chapters

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
    serializer_class = AudioFilesSerializer

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES['audio_file']
        print(audio_file)
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
#         return Response({'status': 'File uploaded successfully'}, status=200)


class AdminView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        # Determine the type of data being added: grade, subject, or chapter
        # 'grade', 'subject', or 'chapter'
        data_type = request.data.get('type')
        print("asdfg")
        print(request.data)

        if data_type == 'grade':
            return self.add_grade(request)
        elif data_type == 'subject':
            return self.add_subject(request)
        elif data_type == 'chapter':
            return self.add_chapter(request)
        elif data_type == 'fecthgrades':
            return self.get_grades(request)
        elif data_type == 'fecthsubjects':
            return self.get_subjects(request)
        elif data_type == 'fetchchapters':
            return self.get_chapters(request)
        else:
            return Response({'error': 'Invalid data type'}, status=status.HTTP_400_BAD_REQUEST)

    def add_grade(self, request):
        print("asdfgh")
        g = request.data.get('grade')
        print(g)
        grade_instance = Grade.objects.create(grade=g)
        serializer = GradeSerializer(grade_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def add_subject(self, request):
        g = request.data.get('grade')
        grade = Grade.objects.get(grade=g)

        sub_name = request.data.get('subject')

        existing_subject = Subject.objects.filter(subjectname=sub_name).first()
        if existing_subject:
            existing_subject2 = grade.subjects.filter(
                subjectname=sub_name).first()
            if (existing_subject2):
                return Response({'error': 'Subject with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

            grade.subjects.add(existing_subject)
            return Response(status=status.HTTP_200_OK)

        subject_instance = Subject.objects.create(name=sub_name)
        grade.subjects.add(subject_instance)

        serializer = SubjectSerializer(subject_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def add_chapter(self, request):
        grade_id = request.data.get('grade')
        subject_id = request.data.get('subject')
        grade = Grade.objects.get(grade=grade_id)
        subject = Subject.objects.get(subjectname=subject_id)
        chap = request.data.get('chapter')
        existing_chapter = Chapter.objects.filter(chaptername=chap).first()
        if existing_chapter:
            existing_chapter_in_subject = Chapters.objects.filter(
                grade=grade, subject=subject, chapters__chaptername=request.data.get('chapter')).first()
            if existing_chapter_in_subject:
                return Response({'error': 'Chapter with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
            existing_subject_of_grade = Chapters.objects.filter(
                grade=grade, subject=subject).first()
            if existing_subject_of_grade:
                existing_subject_of_grade.chapters.add(existing_chapter)
            chapters_instance = Chapters.objects.create(
                grade=grade, subject=subject)

            chapters_instance.chapters.add(existing_chapter)
            return Response(status=status.HTTP_200_OK)

        chapter_instance = Chapter.objects.create(
            chaptername=request.data.get('chapter'))

        existing_subject_of_grade = Chapters.objects.filter(
            grade=grade, subject=subject).first()

        serializer = ChapterSerializer(chapter_instance)
        if existing_subject_of_grade:
            existing_subject_of_grade.chapters.add(chapter_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        chapters_instance = Chapters.objects.create(
            grade=grade, subject=subject)

        chapters_instance.chapters.add(chapter_instance)
        serializer = ChaptersSerializer(chapters_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_grades(self, request):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def get_subjects(self, request):
        try:
            grade = Grade.objects.get(grade=request.data.get('grade'))
        except Grade.DoesNotExist:
            return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)

        subjects = grade.subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def get_chapters(self, request):
        try:
            grade = Grade.objects.get(grade=request.data.get('grade'))
            subject = Subject.objects.get(subjectname=request.data.get('subject'))
        except (Grade.DoesNotExist, Subject.DoesNotExist):
            return Response({'error': 'Grade or Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        
        chapters = Chapters.objects.filter(grade=grade, subject=subject).first().chapters.all()
        
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)
