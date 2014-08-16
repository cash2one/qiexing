# -*- coding: utf-8 -*-

import urllib
import re
import json
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from misc.decorators import staff_required, common_ajax_response, verify_permission

from www.admin.interface import CoverBase


@verify_permission('')
def home(request):
    return HttpResponseRedirect('/admin/sight')


@verify_permission('')
def home_cover(request, template_name='admin/home_cover.html'):
    covers = CoverBase().get_home_cover()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@verify_permission('save_home_cover')
@common_ajax_response
def save_home_cover(request):
    cover = request.REQUEST.get('cover')

    tag_img = re.compile('<img .*?src=[\"\'](.+?)[\"\']')
    imgs = tag_img.findall(cover)

    return CoverBase().save_home_cover(imgs)
