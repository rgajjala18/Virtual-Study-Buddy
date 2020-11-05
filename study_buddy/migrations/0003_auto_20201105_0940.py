# Generated by Django 2.2.10 on 2020-11-05 14:40

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('study_buddy', '0002_auto_20201031_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourse',
            name='preferredFrequency',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('daily', '4-6 times a week'), ('semidaily', '2-3 times a week'), ('weekly', 'Weekly'), ('biweekly', 'Once every two weeks'), ('before_exams', 'Only before exams')], max_length=44),
        ),
        migrations.AlterField(
            model_name='studentcourse',
            name='preferredSize',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('2_people', '2 people total'), ('3_people', '3 people total'), ('4-5_people', '4-5 people total'), ('6_people', '6+ people')], max_length=37),
        ),
        migrations.AlterField(
            model_name='studentcourse',
            name='preferredTimeOfDay',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('early_morning', 'Early mornings (6AM-9AM ET)'), ('mid_morning', 'Mid-morning (9AM-12PM ET)'), ('early_afternoon', 'Early afternoon (12PM-3PM ET)'), ('late_afternoon', 'Late afternoon (3PM-6PM)'), ('evening', 'Evening (6PM-9PM)'), ('night', 'Night (9PM-12AM)')], max_length=70),
        ),
    ]