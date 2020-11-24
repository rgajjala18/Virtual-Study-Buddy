# Generated by Django 2.2.10 on 2020-11-24 19:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_buddy', '0004_auto_20201123_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.BigIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(999999999999)], verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='zoomID',
            field=models.BigIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(999999999999)], verbose_name='Personal Zoom ID'),
        ),
    ]