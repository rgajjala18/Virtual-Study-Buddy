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
    path('groups/<str:id>/', views.group_info, name='group_info'),
    path('groups/<str:id>/<str:sid>/<str:nid>/', views.add_member, name='add_member'),
    path('join/<str:id>/', views.join_group, name='join_group'),
    path('leave/<str:id>/', views.leave_group, name='leave_group'),
    path('remove/<str:id>/<str:sid>/', views.remove_member, name='remove_member'),
    path('show/<str:nid>/', views.show_notif, name='show_notif'),
    path('delete/<str:nid>/', views.delete_notif, name='delete_notif'),
    path('create_notif/<str:sid>/<str:snum>/<str:gnum>/<str:op>/', views.create_notif, name='create_notif'),
]
