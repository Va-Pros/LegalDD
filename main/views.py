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
from core.Parsing import parsing
from core.check_form import check_form
from core.processing import find_key_phrases
from main.logger import *


def process(documents, phrases):
    result = set(phrases)
    for doc in documents:
        result &= set(find_key_phrases(os.path.join(MEDIA_ROOT, doc.file.name), phrases))
        doc.isFinished = True
        doc.save()
    return result


@log_post_params
@csrf_protect
def check_poll(request):
    ogrn = request.POST.get("OGRN")
    data = {"ОГРН":ogrn,
            "ИНН":request.POST.get("INN"),
            "Полное наименование": request.POST.get("fullName"),
            "Сокращенное наименование":request.POST.get("shortName"),
            "Размер уставного капитала":request.POST.get("capital")}
    print(data.values())
    for elem in data.values():
        if elem is None:
            return HttpResponseBadRequest('Часть полей не заполнена')
    name = os.path.join(MEDIA_ROOT, ogrn + '_result.pdf')
    if not downloadPDF(ogrn, name):
        return HttpResponseBadRequest('Не удалось найти огранизацию, проверьте введённый ОГРН')
    parsed = parsing(name)
    os.remove(name)
    if check_form(data, parsed):
        return redirect('/upload')
    return HttpResponseBadRequest('Данные не соответствуют данным, полученным из ЕГРЮЛ на основе введённого ОГРН')
    

class UploadDocument(View):
    @method_decorator(log_get_params)
    def get(self, request):
        return render(
            request,
            'upload.html'
        )
    
    @method_decorator(log_post_params)
    def post(self, request):
        try:
            phraseCnt = int(request.POST.get('phraseCnt'))
        except:
            return HttpResponseBadRequest('Ошибка в запросе')
        phrases = []
        for i in range(phraseCnt):
            phrase = request.POST.get('phrase' + str(i))
            if phrase is None:
                return HttpResponseBadRequest('Ошибка в запросе')
            phrases.append(phrase)
        case = Case()
        case.save()
        files = []
        for file in request.FILES.items():
            doc = Document(file=file[1], originalName=file[0], case=case)
            doc.save()
            files.append(doc)
        result = process(files, phrases)
        string = String(value='\n'.join(result), case=case)
        string.save()
        return redirect('/edit/' + case.name + '/')


@log_get_params
def document_view(request, name):
    file = Document.objects.get(file=name)
    if not file.isFinished:
        return HttpResponse('Файл обрабатывается')
    response = HttpResponse(open(os.path.join(MEDIA_ROOT, name), 'rb'), 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + file.file.name + '"'
    return response


@log_get_params
def edit_view(request, name):
    case = get_object_or_404(Case, name=name)
    notFound = String.objects.get(case=case)
    if notFound is None:
        notFound = []
    else:
        notFound = notFound.value.split('\n')   
    return render(
        request,
        'edit.html',
        {
            'documents': Document.objects.filter(case=case),
            'caseName': name,
            'notFound': notFound,
        })


@log_get_params
def poll_view(request):
    return render(
        request,
        'poll.html'
    )


@log_get_params
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
@log_get_params
def admin_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access denied')
    return render(
        request,
        'admin.html'
    )
