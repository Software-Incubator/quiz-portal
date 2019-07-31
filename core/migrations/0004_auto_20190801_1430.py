# Generated by Django 2.1.5 on 2019-08-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190731_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='university_roll_no',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
