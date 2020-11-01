from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'study_buddy'
urlpatterns = [
    path('', views.home_page, name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update_profile/', views.update_profile, name='update_profile'),
    path('profile/add_course/',
         views.StudentCourseCreate.as_view(), name='add_course'),
    path('profile/update_course/<int:pk>/',
         views.StudentCourseUpdate.as_view(), name='update_course'),
]
