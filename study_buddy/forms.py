from django.forms import ModelForm
from .models import Student, StudentCourse
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from .custom_layout_object import *
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', )


class ProfileForm(ModelForm):
    class Meta:
        model = Student
        fields = ('firstName', 'lastName', 'computingID',
                  'phone', 'zoomID', 'graduationYear', 'bio')


class StudentCourseForm(ModelForm):
    class Meta:
        model = StudentCourse
        exclude = ()


StudentCourseFormSet = inlineformset_factory(
    Student, StudentCourse, form=StudentCourseForm,
    fields=['prefix', 'number', 'preferredSize', 'preferredFrequency', 'preferredTimeOfDay'], extra=1
)
