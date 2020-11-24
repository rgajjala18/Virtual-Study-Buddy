# Generated by Django 2.2.10 on 2020-11-24 19:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_buddy', '0005_auto_20201124_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(999999999999)], verbose_name='Phone Number'),
        ),
    ]
