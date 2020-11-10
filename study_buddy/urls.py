from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'study_buddy'
urlpatterns = [
    path('', views.home_page, name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update_profile/', views.update_profile, name='update_profile'),
    path('profile/update_courses/',
         views.StudentCourseUpdate.as_view(), name='update_courses'),
    path('course/<str:course_prefix>/<int:course_number>/',
         views.course_view, name='course_page'),
    path('course/create_group/',
         views.create_study_group, name='create_group'),
    path('groups/', views.group_view, name='group_page'),
]
