# -*- coding: utf-8 -*-

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from www.sight import interface
sb = interface.SightBase()


def sight_map(request, template_name="sight/sight_map.html"):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def sight_detail(request, sight_id=None, template_name="sight/sight_detail.html"):
    sight = sb.get_sight_by_id(sight_id)
    if not sight:
        raise Http404

    sight = sb.format_sights([sight, ])[0]

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
