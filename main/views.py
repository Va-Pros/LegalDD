from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from main.templates import *
from main.forms import *
from main.models import *
from LegalDD.settings import MEDIA_ROOT
from core.DownloadPDF import downloadPDF

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
            'cases': []#Case.objects.filter(caseType.author=user),
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
            return HttpResponseForbidden('Only admin can add users')
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


class DemoView(View):
    def get(self, request):
        return render(
            request,
            'demo.html'
        )
    
    @method_decorator(csrf_protect)
    def post(self, request):
        ogrn = request.POST.get('data')
        if ogrn is None:
            return HttpResponseBadRequest('Не указано значение')
        downloadPDF(int(ogrn))
        return redirect('/demo')