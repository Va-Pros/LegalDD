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
            return HttpResponseBadRequest('Неверный логин или пароль')
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
            return HttpResponseBadRequest('Не удалось загрузить файл')
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
        return HttpResponseForbidden('Вы не имеете доступ к данному файлу')
    response = HttpResponse("", file.content_type)
    response['Content-Disposition'] = 'attachment; filename="' + file.file.name + '"'
    return response

class AddUser(View):
    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('Доступ запрещён')
        return render(
            request,
            'adduser.html'
        )
    
    @method_decorator(csrf_protect)
    def post(self, request):
        if request.POST['password'] != request.POST['repeat']:
            return HttpResponseBadRequest('Пароли не совпадают')
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
        if request.GET.get('id') is not None:
            profile = get_object_or_404(Profile,
                                        author=user,
                                        id=request.GET['id'])
            return render(
                request,
                'newProfile.html',
                {
                    'id': profile.id,
                    'name': profile.name,
                    'profile_rules': profile.rules.all(),
                    'profile_rule_count': profile.rules.count(),
                    'rules': Rule.objects.filter(author=user),
                })
        else:
            return render(
                request,
                'newProfile.html',
                {
                    'id': -1,
                    'name': "",
                    'profile_rules': [],
                    'profile_rule_count': 0,
                    'rules': Rule.objects.filter(author=user),
                })                
    
    @method_decorator(csrf_protect)
    def post(self, request):
        user = get_object_or_404(UserProfile,
                                 user=request.user)
        if not user.is_lawyer:
            return HttpResponseForbidden('Только юристы могут создавать и редактировать профили')
        # Считаем правила из запроса и проверим их наличие
        rule_count = request.POST.get('rule_count')
        if rule_count is None:
            return HttpResponseBadRequest('Не указано количество правил.')
        rules = []
        for i in range(1, int(rule_count) + 1):
            rule = request.POST.get('rule' + str(i))
            if rule is None:
                return HttpResponseBadRequest('Указано слишком маленькое количество правил.')
            rule = get_object_or_404(Rule,
                                     author=user,
                                     name=rule)
            rules.append(rule)
        # Заполним значения модели и сохраним
        profile_id = request.POST.get('profile_id')
        if profile_id is not None:
            profile = get_object_or_404(Profile,
                                        id=profile_id,
                                        author=user)
        else:
            profile = Profile(author=user)
        profileName = request.POST.get('name')
        if profileName is None:
            return HttpResponseBadRequest('Не указан параметр name.')
        profile.name = profileName
        profile.save()
        profile.rules.set(rules)
        profile.save()
        return redirect('/')
    
def admin_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access denied')
    return render(
        request,
        'admin.html'
    )
