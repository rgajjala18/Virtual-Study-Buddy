from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


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

    #profileIsComplete = models.BooleanField()

    def __str__(self):
        return (self.firstName + " " + self.lastName)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.student.save()
    except ObjectDoesNotExist:
        Student.objects.create(user=instance)


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=4)
    number = models.IntegerField()
    preferredSize = models.CharField(max_length=30)
    preferredFrequency = models.CharField(max_length=30)
    preferredTimeOfDay = models.CharField(max_length=30)

    def __str__(self):
        return (self.prefix + " " + self.number)


class Course(models.Model):
    prefix = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    title = models.CharField(max_length=100, default="")
    students = models.ManyToManyField('study_buddy.Student',
                                      related_name='students')

    def __str__(self):
        return (self.prefix + " " + self.number)
