from django.urls import path
from audiofiles import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns =[
    path('audiofiles/',views.AudioFilesView.as_view()),
    path('audiofiles/add',views.AddAudioFilesView.as_view()),
    path('audiofiles/<ChapterName>',views.selectedView.as_view()),
    path('audiofiles/id/<id>',views.idView.as_view()),
    path('audiofiles/approve/<int:audiofile_id>/', views.ApproveAudioFilesView.as_view(), name='approve-audiofile'),
    path('audiofiles/disapprove/<int:audiofile_id>/', views.DisApproveAudioFilesView.as_view(), name='disapprove-audiofile'),
    
    path('audiofiles/approved/', views.ApprovedAudioFilesView.as_view(), name='approved-audiofiles'),
    path('audiofiles/notapproved/', views.NotApprovedAudioFilesView.as_view(), name='notapproved-audiofiles'),
    path('audiofiles/disapproved/', views.DisApprovedAudioFilesView.as_view(), name='disapproved-audiofiles'),
    
    path('audiofiles/add-data/', views.AdminView.as_view(), name='audiofiles-add-data'),
    path('audiofiles/fetch-data/', views.AdminView.as_view(), name='audiofiles-fetch-data'),
    
]

