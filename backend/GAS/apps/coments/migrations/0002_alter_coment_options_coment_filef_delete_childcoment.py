# Generated by Django 4.2.7 on 2023-11-23 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coment',
            options={'verbose_name': 'Коментарий', 'verbose_name_plural': 'Коментарии'},
        ),
        migrations.AddField(
            model_name='coment',
            name='fileF',
            field=models.FileField(default=0, upload_to='', verbose_name='Файл'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='childComent',
        ),
    ]