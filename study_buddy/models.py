from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from multiselectfield import MultiSelectField


PREFERRED_SIZE_CHOICES = (('2_people', '2 people total'),
                          ('3_people', '3 people total'),
                          ('4-5_people', '4-5 people total'),
                          ('6_people', '6+ people'))

PREFERRED_FREQUENCY_CHOICES = (('daily', '4-6 times a week'),
                               ('semidaily', '2-3 times a week'),
                               ('weekly', 'Weekly'),
                               ('biweekly', 'Once every two weeks'),
                               ('before_exams', 'Only before exams'))

PREFERRED_TIME_OF_DAY_CHOICES = (('early_morning', 'Early mornings (6AM-9AM ET)'),
                                 ('mid_morning', 'Mid-morning (9AM-12PM ET)'),
                                 ('early_afternoon', 'Early afternoon (12PM-3PM ET)'),
                                 ('late_afternoon', 'Late afternoon (3PM-6PM)'),
                                 ('evening', 'Evening (6PM-9PM)'),
                                 ('night', 'Night (9PM-12AM)'))


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstName = models.CharField(max_length=20, verbose_name="First Name")
    lastName = models.CharField(max_length=20, verbose_name="Last Name")
    computingID = models.CharField(max_length=8, verbose_name="Computing ID")
    email = models.EmailField(max_length=254, verbose_name="Email Address")
    phone = models.CharField(max_length=12, verbose_name="Phone Number")
    zoomID = models.CharField(max_length=11, verbose_name="Personal Zoom ID")
    graduationYear = models.IntegerField(
        null=True, verbose_name="Graduation Year")
    bio = models.CharField(max_length=4000, verbose_name="Bio")
    # courseList = ...
    # profileIsComplete = models.BooleanField()

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


class StudentCourse(models.Model):
    student = models.ForeignKey(
        Student, related_name="has_courses", on_delete=models.CASCADE)
    prefix = models.CharField(max_length=4)
    number = models.IntegerField()
    preferredSize = MultiSelectField(choices=PREFERRED_SIZE_CHOICES)
    preferredFrequency = MultiSelectField(choices=PREFERRED_FREQUENCY_CHOICES)
    preferredTimeOfDay = MultiSelectField(
        choices=PREFERRED_TIME_OF_DAY_CHOICES)

    class Meta:
        unique_together = ["student", "prefix", "number"]

    def __str__(self):
        return (self.prefix + " " + str(self.number))


class Course(models.Model):
    prefix = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    title = models.CharField(max_length=100)
    students = models.ManyToManyField('study_buddy.Student',
                                      related_name='students')

    def __str__(self):
        return (self.prefix + " " + self.number)


class StudyGroup(models.Model):
    students = models.ManyToManyField(
        'study_buddy.Student', related_name='students_in_group')
    prefix = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
