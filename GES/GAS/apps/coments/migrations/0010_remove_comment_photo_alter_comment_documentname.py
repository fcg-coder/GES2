# Generated by Django 4.2.7 on 2023-11-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coments', '0009_comment_photo_alter_comment_documentname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='photo',
        ),
        migrations.AlterField(
            model_name='comment',
            name='documentName',
            field=models.CharField(max_length=50, verbose_name='Имя файла'),
        ),
    ]
