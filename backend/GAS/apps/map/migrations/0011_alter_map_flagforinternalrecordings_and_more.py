# Generated by Django 4.2.7 on 2023-12-27 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0010_map_flagforthepresenceofaparent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='FlagForInternalRecordings',
            field=models.IntegerField(verbose_name='Флаг на наличие внутренних записей'),
        ),
        migrations.AlterField(
            model_name='map',
            name='FlagForThePresenceOfAParent',
            field=models.IntegerField(verbose_name='Флаг на наличие родителя'),
        ),
    ]
