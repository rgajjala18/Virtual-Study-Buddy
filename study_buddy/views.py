from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from .forms import *
# Create your views here.


def home_page(request):
    template_name = 'study_buddy/index.html'
    return render(request, template_name)


class StudentCreateView(CreateView):
    model = Student
    fields = ['firstName', 'lastName', 'computingID',
              'email', 'phone', 'zoomID', 'graduationYear', 'bio']
    template_name = 'study_buddy/update_profile.html'


def profile_view(request):
    template_name = 'study_buddy/profile.html'
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

    return render(request, 'study_buddy/update_profile.html', context)


class StudentCourseCreate(CreateView):
    model = StudentCourse
    fields = ['prefix', 'number', 'preferredSize',
              'preferredFrequency', 'preferredTimeOfDay']
    success_url = reverse_lazy('study_buddy:profile')

    def get_context_data(self, **kwargs):
        data = super(StudentCourseCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['studentcourses'] = StudentCourseFormSet(self.request.POST)
        else:
            data['studentcourses'] = StudentCourseFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        studentcourses = context['studentcourses']
        with transaction.atomic():
            form.instance.student = self.request.user.student
            self.object = form.save()

            if studentcourses.is_valid():
                studentcourses.instance = self.object
                studentcourses.save()
        return super(StudentCourseCreate, self).form_valid(form)


class StudentCourseUpdate(UpdateView):
    model = StudentCourse
    fields = ['prefix', 'number', 'preferredSize',
              'preferredFrequency', 'preferredTimeOfDay']
    success_url = reverse_lazy('study_buddy:profile')

    def get_context_data(self, **kwargs):
        data = super(StudentCourseUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['studentcourses'] = StudentCourseFormSet(
                self.request.POST, instance=self.object)
        else:
            data['studentcourses'] = StudentCourseFormSet(
                instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        studentcourses = context['studentcourses']
        with transaction.atomic():
            form.instance.student = self.request.user.student
            self.object = form.save()

            if studentcourses.is_valid():
                studentcourses.instance = self.object
                studentcourses.save()
        return super(StudentCourseUpdate, self).form_valid(form)
