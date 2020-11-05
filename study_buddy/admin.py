from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    fieldsets = [('First Name', {'fields': ['firstName']}),
                 ('Last Name', {'fields': ['lastName']}),
                 ('Email', {'fields': ['email']}), ]
    list_display = ('firstName', 'lastName', 'email')
    search_fields = ['firstName', 'lastName']


class StudentCourseAdmin(admin.ModelAdmin):
    fieldsets = [('Course Mnemonic', {'fields': ['prefix']}),
                 ('Course Number', {'fields': ['number']}),
                 ('Student', {'fields': ['student']}), ]
    list_display = ('prefix', 'number', 'student')
    search_fields = ['prefix', 'number', 'student']


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [('Course Mnemonic', {'fields': ['prefix']}),
                 ('Course Number', {'fields': ['number']}),
                 ('Course Title', {'fields': ['title']}), ]
    list_display = ('prefix', 'number', 'title')
    search_fields = ['prefix', 'number', 'title']


admin.site.register(Student, StudentAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(Course, CourseAdmin)
