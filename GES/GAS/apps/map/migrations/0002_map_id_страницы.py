# Generated by Django 4.2.7 on 2023-11-27 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='Id страницы',
            field=models.IntegerField(default=0, verbose_name='id'),
            preserve_default=False,
        ),
    ]
