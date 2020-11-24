from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', )


class ProfileForm(ModelForm):
    class Meta:
        model = Student
        fields = ('firstName', 'lastName', 'computingID',
                  'phone', 'zoomID', 'graduationYear', 'bio')
    bio = forms.CharField(widget=forms.Textarea)


class StudentCourseForm(ModelForm):
    class Meta:
        model = StudentCourse
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(StudentCourseForm, self).__init__(*args, **kwargs)
        self.fields['prefix'].widget.attrs['style'] = 'width:100px; height:40px'
        self.fields['number'].widget.attrs['style'] = 'width:100px; height:40px'


class StudyGroupForm(ModelForm):
    class Meta:
        model = StudyGroup
        fields = ('studentCourse', 'courseName', 'groupName')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        student = Student.objects.get(user=user)
        self.fields['studentCourse'].queryset = StudentCourse.objects.filter(
            student=student)


StudentCourseFormSet = inlineformset_factory(
    Student, StudentCourse, form=StudentCourseForm,
    fields=['prefix', 'number', 'preferredSize', 'preferredFrequency', 'preferredTimeOfDay'], extra=1
)
