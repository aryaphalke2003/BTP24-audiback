from django.db import models
from django_mysql.models import ListCharField
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


def user_files(instance, filename):
    return 'post_files/{0}/{1}/{2}'.format(instance.pid,instance.title, filename)

# Create your models here.
class Post(models.Model):
    pid = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    pemail = models.CharField(max_length=200)
    description = models.TextField()
    puid = models.CharField(max_length=50)
    className = models.CharField(max_length=120, default=None)
    subjectName = models.CharField(max_length=120, default=None)
    chapterName = models.CharField(max_length=120, default=None)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_users = models.TextField(default=" ")
    disliked_users = models.TextField(default=" ")
    files = models.FileField(upload_to=user_files, storage=gd_storage,null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"
        verbose_name_plural = "posts"
        # unique_together=(("className", "subjectName","chapterName"),)

# class AllUsers(models.Model):
#     uid= models.CharField(max_length=50)

#     def __str__(self):
#         return self.uid

#     class Meta:
#         verbose_name_plural="allusers"
