from django.contrib import admin
from .models import Quiz, Questions, Answer
# Register your models here.

class AnswerInline(admin.TabularInline):
    model=Answer

class QuestionInline(admin.TabularInline):
    model=Questions

class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerInline]

class QuizAdmin(admin.ModelAdmin):
    inlines=[QuestionInline]

admin.site.register(Quiz,QuizAdmin)
admin.site.register(Questions,QuestionAdmin)
admin.site.register(Answer)