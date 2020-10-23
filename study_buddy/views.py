from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from .models import Student
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from .forms import UserForm, ProfileForm
# Create your views here.


class StudentCreateView(CreateView):
    model = Student
    fields = ['firstName', 'lastName', 'computingID',
              'email', 'phone', 'zoomID', 'graduationYear', 'bio']
    template_name = 'study_buddy/updateProfile.html'


def profile_view(request):
    template_name = 'study_buddy/profileView.html'
    student = request.user.student
    return render(request, template_name, {
        'student': student,
    })


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.student)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        messages.success(request, ('Your account has been updated!'))
        return redirect('/study_buddy/profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.student)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'study_buddy/profile.html', context)
