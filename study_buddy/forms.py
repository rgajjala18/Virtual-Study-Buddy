from django.forms import ModelForm
from .models import Student
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', )


class ProfileForm(ModelForm):
    class Meta:
        model = Student
        fields = ('firstName', 'lastName', 'computingID',
                  'phone', 'zoomID', 'graduationYear', 'bio')
