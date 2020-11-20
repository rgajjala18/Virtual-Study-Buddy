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
    notifications = Notification.objects.none()
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        notifications = Notification.objects.filter(student=student, viewed=False)

    return render(request, template_name,{
        "notifications":notifications,
    })



@login_required
def create_notif(request, **kwargs):
    student_query = Student.objects.filter(id=kwargs['sid'])
    student = student_query.first()

    studentNum = kwargs['snum']
    req_query = Student.objects.filter(id=studentNum)
    req = student_query.first()
    groupNum = kwargs['gnum']
    group_query = StudyGroup.objects.filter(id=groupNum)
    group = group_query.first()

    current_student = Student.objects.get(user=request.user)
    operation = kwargs['op']
    title=""
    current_title=""

    if kwargs['op']=='Request':
        title = str(current_student) + " would like to join " + group.groupName + "!"
        current_title = "You requested to join " + str(group.owner) + "'s \'" + group.groupName + "\' study group."
    elif kwargs['op']=='Invite':
        title = str(current_student) + " has invited you to " + group.groupName + "!"
        current_title = "You invited " + str(req) + " to your \'" + group.groupName + "\' study group."

    Notification.objects.create(student=student, title=title, studentNum=studentNum, groupNum=groupNum, viewed=False, operation=operation)
    Notification.objects.create(student=current_student, title=current_title, viewed=False, operation="void")
    return redirect('/study_buddy/groups/')


def show_notif(request, **kwargs):
    template_name = 'study_buddy/notification.html'
    n = Notification.objects.get(id=kwargs['nid'])
    groupNum = n.groupNum
    group_query = StudyGroup.objects.filter(id=groupNum)
    group = group_query.first()

    return render(request, template_name, {'notification' : n, 'group' : group,})

def delete_notif(request, **kwargs):
    n = Notification.objects.get(id=kwargs['nid'])
    n.viewed = True
    n.save()
    return redirect('/study_buddy/')



@login_required
def create_study_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.user, request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            new_student = Student.objects.get(user=request.user)
            group.students.add(new_student)
            group.owner = new_student
            group.save()
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
    student = Student.objects.get(user=request.user)

    return render(request, template_name, {
        'course': course_query,
        'student': request.user,
        'student_object': student,
        'study_groups': study_groups,
    })

def group_view(request, **kwargs):
    template_name = 'study_buddy/group_view.html'
    student = Student.objects.get(user=request.user)
    study_groups = student.studygroup_set.all()

    return render(request, template_name, {
        'student': request.user,
        'study_groups': study_groups,
    })

def group_info(request, **kwargs):
    template_name = 'study_buddy/group_info.html'
    group_query = StudyGroup.objects.filter(id=kwargs['id'])
    group = group_query.first()
    studentsInGroup = group.students.all()
    course = group.studentCourse
    studentsInClass = StudentCourse.objects.filter(prefix=course.prefix, number=course.number)
    student = Student.objects.get(user=request.user)
    if student not in studentsInGroup:
        return redirect('/study_buddy/groups/')

    return render(request, template_name, {
        'group': group,
        'student': student,
        'students': studentsInGroup,
        'students_in_class' : studentsInClass,
    })


def add_member(request, **kwargs):
    group_query = StudyGroup.objects.filter(id=kwargs['id'])
    group = group_query.first()
    student_query = Student.objects.filter(id=kwargs['sid'])
    student = student_query.first()
    notif_query = Notification.objects.filter(id=kwargs['nid'])
    notif = student_query.first()
    notif.viewed = True
    notif.save()
    group.students.add(student)
    return redirect('/study_buddy/groups/' + kwargs['id'] + '/')


def remove_member(request, **kwargs):
    group_query = StudyGroup.objects.filter(id=kwargs['id'])
    group = group_query.first()
    student_query = Student.objects.filter(id=kwargs['sid'])
    student = student_query.first()
    group.students.remove(student)
    return redirect('/study_buddy/groups/' + kwargs['id'] + '/')


def join_group(request, **kwargs):
    student = Student.objects.get(user=request.user)
    group_query = StudyGroup.objects.filter(id=kwargs['id'])
    group = group_query.first()
    group.students.add(student)
    return redirect('/study_buddy/groups/')


def leave_group(request, **kwargs):
    group_query = StudyGroup.objects.filter(id=kwargs['id'])
    group = group_query.first()
    student = Student.objects.get(user=request.user)
    group.students.remove(student)
    if student.id == group.owner.id:
        group.owner = group.students.first()
        group.save()
    return redirect('/study_buddy/groups/')





    
