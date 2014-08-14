# -*- coding: utf-8 -*-

import urllib
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response


def home(request):
    return HttpResponseRedirect('/admin/sight')
