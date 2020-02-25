"""LegalDD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(lk_view)),
    path('', RedirectView.as_view(url='login')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('upload/', login_required(UploadDocument.as_view())),
    path('documents/<str:name>/', login_required(document_view)),
    path('adduser/', login_required(AddUser.as_view())),
]
