# Generated by Django 4.2.1 on 2024-02-18 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audiofiles', '0003_chapter_subject_alter_audiofiles_audiofile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofiles',
            name='Class',
        ),
    ]
