# -*- coding: utf-8 -*-

# from django.contrib import auth
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response


def home(request, template_name='journey/home.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def journey_list(request, template_name='journey/journey_list.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
