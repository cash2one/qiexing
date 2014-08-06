# -*- coding: utf-8 -*-

# from django.contrib import auth
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response


def activity_list(request, template_name='activity/activity_list.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def activity_detail(request, activity_id=None, template_name='activity/activity_detail.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def launch_activity(request, template_name='activity/launch_activity.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
