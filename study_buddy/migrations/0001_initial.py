# Generated by Django 3.1.1 on 2020-10-23 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=20, verbose_name='First Name')),
                ('lastName', models.CharField(max_length=20, verbose_name='Last Name')),
                ('computingID', models.CharField(max_length=8, verbose_name='Computing ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('phone', models.CharField(max_length=12, verbose_name='Phone Number')),
                ('zoomID', models.CharField(max_length=11, verbose_name='Personal Zoom ID')),
                ('graduationYear', models.IntegerField(null=True, verbose_name='Graduation Year')),
                ('bio', models.CharField(max_length=4000, verbose_name='Bio')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=4)),
                ('number', models.IntegerField()),
                ('preferredSize', models.CharField(max_length=30)),
                ('preferredFrequency', models.CharField(max_length=30)),
                ('preferredTimeOfDay', models.CharField(max_length=30)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_buddy.student')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=6)),
                ('title', models.CharField(max_length=100)),
                ('students', models.ManyToManyField(related_name='students', to='study_buddy.Student')),
            ],
        ),
    ]
