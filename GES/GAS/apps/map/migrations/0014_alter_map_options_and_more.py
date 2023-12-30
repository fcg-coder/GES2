# Generated by Django 4.2.7 on 2023-12-30 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0013_map_flagforinternalrecordings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='map',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='map',
            name='FlagForInternalRecordings',
            field=models.IntegerField(verbose_name='Флаг на наличие подкатегорий'),
        ),
        migrations.AlterField(
            model_name='map',
            name='FlagForThePresenceOfAParent',
            field=models.IntegerField(verbose_name='Флаг на наличие родительской категории'),
        ),
    ]
