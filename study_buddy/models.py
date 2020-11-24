from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


PREFERRED_SIZE_CHOICES = (('2_people', ' 2 people total'),
                          ('3_people', ' 3 people total'),
                          ('4-5_people', ' 4-5 people total'),
                          ('6_people', ' 6+ people'))

PREFERRED_FREQUENCY_CHOICES = (('daily', ' 4-6 times a week'),
                               ('semidaily', ' 2-3 times a week'),
                               ('weekly', ' Weekly'),
                               ('biweekly', ' Every two weeks'),
                               ('before_exams', ' Before exams'))

PREFERRED_TIME_OF_DAY_CHOICES = (('early_morning', ' 6AM-9AM'),
                                 ('mid_morning', ' 9AM-12PM'),
                                 ('early_afternoon', ' 12PM-3PM'),
                                 ('late_afternoon', ' 3PM-6PM'),
                                 ('evening', ' 6PM-9PM'),
                                 ('night', ' 9PM-12AM'))


class Notification(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    operation = models.CharField(max_length=10, verbose_name="Operation")
    viewed = models.BooleanField(default=False)
    studentNum = models.CharField(max_length=10, null=True)
    groupNum = models.CharField(max_length=10, null=True)
    student = models.ForeignKey(
        'Student', on_delete=models.SET_NULL, null=True, verbose_name="Student")


class StudyGroup(models.Model):
    owner = models.ForeignKey('Student', on_delete=models.SET_NULL,
                              null=True, verbose_name="Owner", related_name='has_owner')
    students = models.ManyToManyField('Student')
    studentCourse = models.ForeignKey(
        'StudentCourse', on_delete=models.SET_NULL, null=True, verbose_name="Course")
    courseName = models.CharField(
        max_length=30, verbose_name="Course Name", default="")
    groupName = models.CharField(
        max_length=100, verbose_name="Group Name", default="")

    def student_names(self):
        return ', '.join([str(s) for s in self.students.all()])
    student_names.short_description = "Student Names"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstName = models.CharField(max_length=20, verbose_name="First Name")
    lastName = models.CharField(max_length=20, verbose_name="Last Name")
    computingID = models.CharField(max_length=8, verbose_name="Computing ID", validators=[
                                   RegexValidator(regex='[a-z][a-z][a-z]?[0-9][a-z][a-z][a-z]?', message='Invalid computing ID'), ])
    email = models.EmailField(max_length=254, verbose_name="Email Address")
    phone = models.BigIntegerField(verbose_name="Phone Number", validators=[
        MaxValueValidator(999999999999)])
    zoomID = models.BigIntegerField(verbose_name="Personal Zoom ID", validators=[
        MaxValueValidator(999999999999)])
    graduationYear = models.IntegerField(
        null=True, verbose_name="Graduation Year", validators=[MinValueValidator(datetime.date.today().year), MaxValueValidator(datetime.date.today().year + 8)])
    bio = models.CharField(max_length=4000, verbose_name="Bio")

    def __str__(self):
        return (self.firstName + " " + self.lastName)


@ receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@ receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.student.save()
    except ObjectDoesNotExist:
        Student.objects.create(user=instance)


class Course(models.Model):
    prefix = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    title = models.CharField(max_length=100)
    students = models.ManyToManyField('study_buddy.Student',
                                      related_name='students')

    def __str__(self):
        return (self.prefix + " " + self.number)


class StudentCourse(models.Model):
    student = models.ForeignKey(
        Student, related_name="has_courses", on_delete=models.CASCADE)
    prefix = models.CharField(max_length=4)
    number = models.IntegerField()
    preferredSize = MultiSelectField(
        choices=PREFERRED_SIZE_CHOICES, verbose_name="Preferred Size")
    preferredFrequency = MultiSelectField(
        choices=PREFERRED_FREQUENCY_CHOICES, verbose_name="Preferred Frequency")
    preferredTimeOfDay = MultiSelectField(
        choices=PREFERRED_TIME_OF_DAY_CHOICES, verbose_name="Preferred Time")

    class Meta:
        unique_together = ["student", "prefix", "number"]

    def __str__(self):
        return (self.prefix + " " + str(self.number))

    def clean(self, *args, **kwargs):
        courses = Course.objects.filter(prefix=self.prefix, number=self.number)
        if len(courses) == 0:
            raise ValidationError(
                _('Not a valid course'),
                params={'prefix': self.prefix, 'number': self.number},
            )
