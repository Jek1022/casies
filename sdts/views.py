#__author__ = 'reykennethmolina'

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect, Http404

def active_menu(request):
    return {'active_menu': request.path}
