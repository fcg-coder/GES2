# Generated by Django 4.2.7 on 2023-12-31 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0014_alter_map_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='nameOfPage',
        ),
        migrations.RemoveField(
            model_name='map',
            name='status',
        ),
    ]