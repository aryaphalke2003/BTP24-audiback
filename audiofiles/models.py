from django.db import models
from django.utils import timezone
from gdstorage.storage import GoogleDriveStorage
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission
from django.core.validators import MinValueValidator, MaxValueValidator

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
# gd_storage = GoogleDriveStorage()

# Create your models here.
def user_directory_path(instance,filename):
    print(instance.id,filename)
    return 'audiofiles/{1}'.format(instance.id,filename)

def file_path(instance,filename):
    return 'pdf_chapters/{1}'.format(instance.id,filename)

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # Storing hashed passwords
    
    class Meta:
        # db_table = "audiofiles"
        verbose_name_plural="admins"

   
    
    
 

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
    Author=models.CharField(max_length=100,default='')
    description=models.CharField(max_length=1000, default='')
    References=models.CharField(max_length=1000,default='')
    approvedBy=models.ForeignKey(Admin,on_delete=models.CASCADE, null=True)
    is_disapproved=models.BooleanField(default=False)


    # def admin_name(self):
    #     return self.approvedBy.name if self.approvedBy else None

    # def __str__(self):
    #     return f"{self.id} - {self.ChapterName} - Approved by: {self.admin_name()}"

    class Meta:
        # db_table = "audiofiles"
        verbose_name_plural="audiofiles"
        # unique_together=(("title", "audio"),)
    

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subjectname = models.CharField(max_length=100,default='')
  

    class Meta:
        # db_table = "audiofiles"
        verbose_name_plural="subjects"
            
class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    chaptername = models.CharField(max_length=100,default='')
    is_pdf_available = models.BooleanField(default=False)
    is_audiofile_available = models.BooleanField(default=False)
    
    class Meta:
        # db_table = "audiofiles"
        verbose_name_plural="Chapter"
    

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    grade = models.IntegerField(unique=True)
    subjects = models.ManyToManyField(Subject,null=True)
    
    class Meta:
        # db_table = "audiofiles"
        constraints = [
        models.UniqueConstraint(fields=['grade'], name='unique grade')
    ]
        verbose_name_plural="Grades"
    
class Chapters(models.Model):
    id = models.AutoField(primary_key=True)
    
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapters = models.ManyToManyField(Chapter,null=True)
    
    class Meta:
        # db_table = "audiofiles"
        verbose_name_plural="Chapters"
        
        




    