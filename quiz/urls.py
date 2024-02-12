from django.urls import path
from quiz import views

urlpatterns = [
    path('quiz', views.AllQuizView.as_view()),

    path('quiz/<chapterName>', views.QuizView.as_view()),

    path('quiz/<chapterName>/questions', views.QuestionsView.as_view()),
    path('quiz/<chapterName>/questions/<id>', views.QuestionsIdView.as_view()),

    path('quiz/<chapterName>/<qid>/answers/<id>', views.AnswersIdView.as_view()),
    path('quiz/<chapterName>/questions/<qid>/answers',
         views.AnswersView.as_view()),

]
