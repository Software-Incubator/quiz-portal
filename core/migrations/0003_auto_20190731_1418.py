# Generated by Django 2.1.5 on 2019-07-31 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190731_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='phone_number',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(regex='^[56789]\\d{9}$')]),
        ),
    ]
