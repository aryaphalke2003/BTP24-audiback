from django.db import models

# Create your models here.


class Quiz(models.Model):
    className = models.CharField(max_length=120)
    subjectName = models.CharField(max_length=120)
    chapterName = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.className}_{self.subjectName}_{self.chapterName}"

    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name_plural = "Quizes"
        unique_together = (("className", "subjectName", "chapterName"),)


class Questions(models.Model):
    text = models.CharField(max_length=300)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,
                             related_name="questions", null=True, default=None)
    

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answers.all()

    class Meta:
        verbose_name_plural = "Questions"


class Answer(models.Model):
    text = models.CharField(max_length=300)
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name='answers', null=True, default=None)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Answers"
