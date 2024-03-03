from rest_framework import serializers

from .models import AudioFiles
from .models import Grade, Subject, Chapter, Chapters, Admin



# class AudioFilesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AudioFiles
#         fields = "__all__"

class AudioFilesSerializer(serializers.ModelSerializer):
    approvedBy = serializers.SerializerMethodField()

    class Meta:
        model = AudioFiles
        fields = '__all__'

    def get_approvedBy(self, instance):
        if instance.approvedBy:
            return instance.approvedBy.name
        return None

       
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