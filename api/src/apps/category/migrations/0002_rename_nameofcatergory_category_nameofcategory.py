# Generated by Django 4.2.16 on 2024-10-10 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='nameOfCatergory',
            new_name='nameOfCategory',
        ),
    ]