# Generated by Django 2.0.6 on 2018-06-06 11:38

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20180606_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correctchoice',
            name='correct_choice',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
