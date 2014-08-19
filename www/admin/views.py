# -*- coding: utf-8 -*-

import urllib
import re
import json
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from misc.decorators import staff_required, common_ajax_response, verify_permission

from www.admin.interface import StaticPageBase


@verify_permission('')
def home(request):
    return HttpResponseRedirect('/admin/sight')


@verify_permission('save_static_page')
def static_page(request, template_name='admin/static_page.html'):

    if request.method == "POST":

        StaticPageBase().save_static_page(
            request.REQUEST.get('footer_about'),
            request.REQUEST.get('about'),
            request.REQUEST.get('agreement'),
            request.REQUEST.get('contact')
        )

    data = StaticPageBase().get_static_page()

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
