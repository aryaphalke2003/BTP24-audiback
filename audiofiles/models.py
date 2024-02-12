from django.db import models
from django.utils import timezone
from gdstorage.storage import GoogleDriveStorage
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission

permission1 =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.WRITER,
   GoogleDrivePermissionType.USER,
   "2020csb1110@iitrpr.ac.in"
)
permission2 =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.WRITER,
   GoogleDrivePermissionType.USER,
   "2020csb1107@iitrpr.ac.in"
)

gd_storage = GoogleDriveStorage(permissions=(permission1,permission2 ))

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.
def user_directory_path(instance,filename):
    print(instance.id,filename)
    return 'audiofiles/{1}'.format(instance.id,filename)

def file_path(instance,filename):
    return 'pdf_chapters/{1}'.format(instance.id,filename)

class AudioFiles(models.Model):
    id = models.AutoField(primary_key=True)
    # Caption=models.CharField(max_length=100,default='')
    Publish=models.DateTimeField(default=timezone.now)
    Class=models.CharField(max_length=100,default='')
    Subject=models.CharField(max_length=120,default='')
    ChapterName=models.CharField(max_length=100,default='')
    PDF=models.FileField(upload_to=file_path,storage=gd_storage, null=True)
    AudioFile= models.FileField(upload_to=user_directory_path,storage=gd_storage,null=True)
    is_approved = models.BooleanField(default=False)
    # audio_stamps = models.TextField(default=" ")

    class Meta:
        # db_table = "audiofiles"
        verbose_name_plural="audiofiles"
        # unique_together=(("title", "audio"),)
    