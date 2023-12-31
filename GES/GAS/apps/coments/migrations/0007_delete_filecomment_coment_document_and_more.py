# Generated by Django 4.2.7 on 2023-11-24 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coments', '0006_alter_filecomment_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='fileComment',
        ),
        migrations.AddField(
            model_name='coment',
            name='document',
            field=models.FileField(default=0, upload_to='documents/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coment',
            name='documentName',
            field=models.CharField(default=0, max_length=50, verbose_name='Имя'),
            preserve_default=False,
        ),
    ]
