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


def process(string, documents, phrases):
    result = set(phrases)
    for doc in documents:
        result &= set(find_key_phrases(os.path.join(MEDIA_ROOT, doc[0].file.name), phrases, doc[1]))
        doc[0].isFinished = True
        if doc[1] != 'application/pdf':
            name = doc[0].file.name
            doc[0].file.name = '.'.join(name.split('.')[:-1]) + '.pdf'
        doc[0].save()
    string.value = '\n'.join(result)
    string.save()


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
            fileType = request.FILES.get(file[0]).content_type
            if fileType != 'application/pdf':
                doc.file.name += '.docx'
            doc.save()
            files.append((doc, fileType))
        string = String(value='', case=case)
        string.save()
        thr = Thread(target=process, args=(string, files, phrases))
        thr.start()
        return redirect('/edit/' + case.name + '/')


@log_get_params
def document_view(request, uid):
    file = get_object_or_404(Document, uid=uid)
    if not file.isFinished:
        return render(
            request,
            'reload_doc.html'
            )
    response = HttpResponse(open(os.path.join(MEDIA_ROOT, file.file.name), 'rb'), 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + file.file.name + '"'
    return response


@log_get_params
def edit_view(request, name):
    case = get_object_or_404(Case, name=name)
    notFound = String.objects.get(case=case)
    if notFound is None:
        notFoundArr = []
    else:
        notFoundArr = notFound.value.split('\n')   
    return render(
        request,
        'edit.html',
        {
            'documents': Document.objects.filter(case=case),
            'caseName': name,
            'notFoundAny': notFound.value != '',
            'notFound': notFoundArr,
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
