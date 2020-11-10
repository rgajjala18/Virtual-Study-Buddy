from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
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


@login_required
def create_study_group(request):
    """
    if request.method == 'POST':
        study_group_form = StudyGroupForm(request.POST, instance=request.user)
        if study_group_form.is_valid():
            study_group_form.save()
        messages.success(request, ('Your study group has been created!'))
        return redirect('/study_buddy/profile')
    else:
        study_group_form = StudyGroupForm(instance=request.user)

    context = {
        'study_group_form': study_group_form,
    }

    return render(request, 'study_buddy/create_group.html', context)
    """
    if request.method == 'POST':
        form = StudyGroupForm(request.user, request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            new_student = Student.objects.get(user=request.user)
            #group.student = new_student
            #new_student.group = group
            group.save()
            group.students.add(new_student)
            return redirect('/study_buddy/groups')
    else:
        form = StudyGroupForm(request.user)
    return render(request, 'study_buddy/group_form.html', {'form': form})
    



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


class StudentCourseUpdate(UpdateView):
    model = Student
    fields = []
    success_url = reverse_lazy('study_buddy:profile')
    template_name = 'study_buddy/studentcourse_form.html'

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

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.student.pk)


def course_view(request, **kwargs):
    template_name = 'study_buddy/course_view.html'
    course_query = StudentCourse.objects.filter(
        prefix=kwargs['course_prefix'], number=kwargs['course_number'])
    course = course_query.first()
    study_groups = StudyGroup.objects.filter(studentCourse__prefix=course.prefix, studentCourse__number=course.number)

    return render(request, template_name, {
        'course': course_query,
        'student': request.user,
        'study_groups': study_groups,
    })

def group_view(request, **kwargs):
    template_name = 'study_buddy/group_view.html'
    student = Student.objects.get(user=request.user)
    #study_groups = StudyGroup.objects.filter(student__user=request.user.id)
    study_groups = student.studygroup_set.all()

    return render(request, template_name, {
        'student': request.user,
        'study_groups': study_groups,
    })
