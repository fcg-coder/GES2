# Generated by Django 4.2.7 on 2023-11-24 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coments', '0007_delete_filecomment_coment_document_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Coment',
            new_name='Comment',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='coment_text',
            new_name='comment_text',
        ),
    ]
