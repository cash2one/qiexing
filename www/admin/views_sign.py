# -*- coding: utf-8 -*-

import urllib
import json
import re
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from www.misc import qiniu_client
from common import utils, page
from misc.decorators import staff_required, common_ajax_response, verify_permission

from www.activity.interface import ActivityPersonBase, ActivityBase
from www.account.interface import UserBase


# @verify_permission('')
def sign(request, template_name='admin/sign.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def format_sign(objs, num):

    data = []

    for x in objs:
        num += 1

        user = UserBase().get_user_by_id(x.user_id)
        #activity = ActivityBase().get_activity_by_id(need_state=None)

        data.append({
            'num': num,
            'sign_id': x.id,
            'user_id': user.id,
            'user_name': user.nick,
            'activity_id': x.activity.id,
            'activity_name': x.activity.title,
            'real_name': x.real_name,
            'mobile': x.mobile,
            'partner_count': x.partner_count,
            'state': x.state
        })

    return data


# @verify_permission('query_sign')
def search(request):
    data = []
    apb = ActivityPersonBase()

    name = request.REQUEST.get('name')
    state = request.REQUEST.get('state', 0)

    objs = apb.get_sign_infos_for_admin(state, name)

    page_index = int(request.REQUEST.get('page_index'))

    page_objs = page.Cpt(objs, count=10, page=page_index).info

    # 格式化json
    num = 10 * (page_index - 1)
    data = format_sign(page_objs[0], num)

    return HttpResponse(
        json.dumps({'data': data, 'page_count': page_objs[4], 'total_count': page_objs[5]}),
        mimetype='application/json'
    )
