# Generated by Django 4.2.7 on 2023-12-31 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PAGE', '0007_page_id_категории'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='Id категории',
        ),
    ]
