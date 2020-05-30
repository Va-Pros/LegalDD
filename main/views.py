from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

import os
import zipfile
from threading import Thread

from main.templates import *
from main.forms import *
from main.models import *
from LegalDD.settings import MEDIA_ROOT
from core.DownloadPDF import downloadPDF
from main.logger import *


def process(documents):
    for doc in documents:
        print('Processing document', doc.file.name)
        doc.isFinished = True
        doc.save()
    

class UploadDocument(View):
    @method_decorator(log_get_params)
    def get(self, request):
        return render(
            request,
            'upload.html'
        )
    
    @method_decorator(log_post_params)
    def post(self, request):
        case = Case()
        case.save()
        files = []
        for file in request.FILES.items():
            doc = Document(file=file[1], originalName=file[1], case=case)
            doc.save()
            files.append(doc)
        process(files)
        return redirect('/edit/' + case.name + '/')


def document_view(request, name):
    file = Document.objects.get(file=name)
    if not file.isFinished:
        return HttpResponse('Файл обрабатывается')
    response = HttpResponse(open(os.path.join(MEDIA_ROOT, name), 'rb'), 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + file.file.name + '"'
    return response


def edit_view(request, name):
    case = get_object_or_404(Case, name=name)
    return render(
        request,
        'edit.html',
        {
            'documents': Document.objects.filter(case=case),
            'caseName': name,
        })


def download_view(request, name):
    case = get_object_or_404(Case, name=name)
    files = Document.objects.filter(case=case)
    archName = os.path.join(MEDIA_ROOT, name + '.zip')
    archive = zipfile.ZipFile(archName, 'w')
    for file in files:
        archive.write(os.path.join(MEDIA_ROOT, file.file.name), file.originalName)
    archive.close()
    response = HttpResponse(open(archName, 'rb'), 'application/octet-stream')
    os.remove(archName)
    response['Content-Disposition'] = 'attachment; filename="' + name + '.zip"'
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
