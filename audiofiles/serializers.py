from rest_framework import serializers

from .models import AudioFiles


class AudioFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFiles
        fields = "__all__"