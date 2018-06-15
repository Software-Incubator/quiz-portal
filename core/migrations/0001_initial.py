# Generated by Django 2.0.6 on 2018-06-14 17:40

import ckeditor_uploader.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('father_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(regex='^[789]\\d{9}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=225)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
            options={
                'verbose_name_plural': 'Instructions',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveIntegerField(blank=True)),
                ('question_text', ckeditor_uploader.fields.RichTextUploadingField()),
                ('choice1', ckeditor_uploader.fields.RichTextUploadingField()),
                ('choice2', ckeditor_uploader.fields.RichTextUploadingField()),
                ('choice3', ckeditor_uploader.fields.RichTextUploadingField()),
                ('choice4', ckeditor_uploader.fields.RichTextUploadingField()),
                ('correct_choice', models.PositiveIntegerField()),
                ('negative', models.BooleanField(default=False)),
                ('negative_marks', models.IntegerField(blank=True, null=True)),
                ('marks', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Category')),
            ],
        ),
        migrations.CreateModel(
            name='SelectedAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_choice', models.PositiveIntegerField(blank=True)),
                ('status', models.PositiveIntegerField(default=1)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Candidate')),
                ('question_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=100)),
                ('duration', models.PositiveIntegerField()),
                ('on_or_off', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='instruction',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Test'),
        ),
        migrations.AddField(
            model_name='category',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Test'),
        ),
    ]
