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
from main.logger import *
    

class UploadDocument(View):
    @method_decorator(log_get_params)
    def get(self, request):
        return render(
            request,
            'upload.html'
        )
    
    @method_decorator(log_post_params)
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest('Не удалось загрузить файл')
        file = form.save(commit=False)
        file.author = request.user
        file.content_type = request.FILES.getlist('file')[0].content_type
        file.save()
        return redirect('/')

def document_view(request, name):
    file = Document.objects.get(file=name)
    if not (request.user.is_superuser or request.user == file.author):
        return HttpResponseForbidden('Вы не имеете доступ к данному файлу')
    response = HttpResponse("", file.content_type)
    response['Content-Disposition'] = 'attachment; filename="' + file.file.name + '"'
    return response


# Служебная страница
class DemoView(View):
    @method_decorator(log_get_params)
    def get(self, request):
        return render(
            request,
            'demo.html'
        )
    
    @method_decorator(log_post_params)
    @method_decorator(csrf_protect)
    def post(self, request):
        ogrn = request.POST.get('data')
        if ogrn is None:
            return HttpResponseBadRequest('Не указано значение')
        downloadPDF(int(ogrn))
        return redirect('/demo')

# Служебная страница
@log_get_params
def admin_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access denied')
    return render(
        request,
        'admin.html'
    )
