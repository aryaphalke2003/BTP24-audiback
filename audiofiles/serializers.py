from rest_framework import serializers

from .models import AudioFiles
from .models import Grade, Subject, Chapter, Chapters



class AudioFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFiles
        fields = "__all__"
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    
    class Meta:
        model = Grade
        fields = '__all__'

class ChaptersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapters
        fields = '__all__'