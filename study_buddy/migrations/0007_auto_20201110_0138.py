# Generated by Django 3.1.1 on 2020-11-10 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study_buddy', '0006_studygroup_groupname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studygroup',
            name='number',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='prefix',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='students',
        ),
        migrations.AddField(
            model_name='studygroup',
            name='courseName',
            field=models.CharField(default='', max_length=30, verbose_name='Course Name'),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='study_buddy.student'),
        ),
        migrations.AddField(
            model_name='studygroup',
            name='studentCourse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='study_buddy.studentcourse', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='groupName',
            field=models.CharField(default='', max_length=100, verbose_name='Group Name'),
        ),
    ]
