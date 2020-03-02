from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from main.templates import *
from main.forms import *
from main.models import *
from LegalDD.settings import MEDIA_ROOT

class HelloView(View):
    def get(self, request):
        return render(
            request,
            'test.html',
            {
                'name': request.user
            }
        )


class LoginView(View):
    def get(self, request):
        return render(
            request,
            'login.html'
        )
    
    @method_decorator(csrf_protect)
    def post(self, request):
        if request.user.is_anonymous:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            return HttpResponseBadRequest('Login or password incorrect')
        return redirect('/')
    

class UploadDocument(View):
    def get(self, request):
        return render(
            request,
            'upload.html'
        )
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest('File could not be loaded')
        file = form.save(commit=False)
        file.author = request.user
        file.content_type = request.FILES.getlist('file')[0].content_type
        file.save()
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')

def lk_view(request):
    user = UserProfile.objects.get(user=request.user)
    return render(
        request,
        'lk.html',
        {
            'user': user,
            'documents': Document.objects.all(),
            'profiles': Profile.objects.filter(author=user),
        })

def document_view(request, name):
    file = Document.objects.get(file=name)
    if not (request.user.is_superuser or request.user == file.author):
        return HttpResponseForbidden('You are not allowed to view this file')
    response = HttpResponse("", file.content_type)
    response['Content-Disposition'] = 'attachment; filename="' + file.file.name + '"'
    return response

class AddUser(View):
    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('Access denied')
        return render(
            request,
            'adduser.html'
        )
    
    @method_decorator(csrf_protect)
    def post(self, request):
        if request.POST['password'] != request.POST['repeat']:
            return HttpResponseBadRequest('Passwords do not match')
        user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
        user.save()
        profile = UserProfile(user=user)
        profile.is_lawyer = (request.POST.get('is_lawyer') is not None)
        profile.is_curator = (request.POST.get('is_curator') is not None)
        profile.save()
        return redirect('/adduser')

class EditProfile(View):
    def get(self, request):
        user = get_object_or_404(UserProfile,
                                 user=request.user)
        if not user.is_lawyer:
            return HttpResponseForbidden('Только юристы могут создавать и редактировать профили')
        name = ""
        creating = True
        if request.GET.get('name') is not None:
            profile = get_object_or_404(Profile,
                                        author=user,
                                        name=request.GET['name'])
            name = profile.name
            creating = False
        return render(
            request,
            'newProfile.html',
            {
                'creating': creating,
                'name': name,
                'profile_rules': [],
                'rules': Rule.objects.filter(author=user),
            })
    
    @method_decorator(csrf_protect)
    def post(self, request):
        user = get_object_or_404(UserProfile,
                                 user=request.user)
        if not user.is_lawyer:
            return HttpResponseForbidden('Только юристы могут создавать и редактировать профили')
        profileName = request.POST.get('name')
        try:
            print('Trying to get profile', profileName)
            profile = Profile.objects.get(name=profileName)
            print('Got profile', profile=name)
            if profile.user != user:
                return HttpRsponseForbidden('Данный профиль не принадлежит Вам')
            profile.name = profileName
            profile.save()
        except:
            # Профиль не найден, создаём новый
            profile = Profile(author=user)
            profile.name = profileName
            profile.save()
        return redirect('/')
    
def admin_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access denied')
    return render(
        request,
        'admin.html'
    )
