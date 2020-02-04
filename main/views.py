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

# Create your views here
