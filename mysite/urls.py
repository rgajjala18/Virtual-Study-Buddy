"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mysite.views import home_page
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='study_buddy/index.html')),
    path('secure_admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('study_buddy/', include('study_buddy.urls'))
]
