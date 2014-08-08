# -*- coding: utf-8 -*-

import urllib
import json
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response


def sight_map(request, template_name="sight/sight_map.html"):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def sight_detail(request, sight_id=None, template_name="sight/sight_detail.html"):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
