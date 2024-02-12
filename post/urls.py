from django.urls import path
from post import views

urlpatterns =[
    path('post/',views.PostView.as_view()),
    path('post/<chapterName>',views.selectedView.as_view()),
    path('post/id/<id>',views.idView.as_view()),
    path('post/likes/id/<id>',views.LikesDislikesView.as_view()),
]