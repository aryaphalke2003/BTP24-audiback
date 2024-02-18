from django.contrib import admin

# Register your models here.
from .models import AudioFiles 
# Register your models here.
from .models import Grade, Subject, Chapter, Chapters


admin.site.register(AudioFiles)

admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Chapters)
