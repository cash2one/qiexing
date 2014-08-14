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

from www.sight.interface import SightBase


def sight(request, template_name='admin/sight.html'):
    from www.misc.consts import G_PROVINCE
    province_dict = [{'value': G_PROVINCE[x][0], 'name': x} for x in G_PROVINCE.keys()]
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


#@verify_permission('add_stock')
def add_sight(request):
    name = request.REQUEST.get('name')
    province = request.REQUEST.get('province')
    code = request.REQUEST.get('code')
    des = request.REQUEST.get('des')
    cover = request.REQUEST.get('cover')

    tag_img = re.compile('<img .*?src=[\"\'](.+?)[\"\']')
    imgs = tag_img.findall(cover)

    flag, msg = SightBase().add_sight(name, province, des, code, imgs)

    if flag == 0:
        url = "/admin/sight?#modify/%s" % (msg.id)
    else:
        url = "/admin/sight?%s" % (msg)

    return HttpResponseRedirect(url)


def get_province_by_name(request):
    name = request.REQUEST.get('province_name', '')

    result = []

    data = SightBase().get_province_by_name(name)
    if data:
        for k in data.keys():
            result.append([data[k][0], k, None, k])

    return HttpResponse(json.dumps(result), mimetype='application/json')


def format_sight(objs, num):
    from www.misc.consts import G_PROVINCE

    data = []

    for x in objs:
        num += 1
        temp = {}
        imgs = SightBase().get_sight_imgs(x)
        cover = ''
        for i in imgs:
            cover += '<p><img src="%s"/></p>' % i.img

        p = filter(lambda k: str(G_PROVINCE[k][0]) == x.province_key, G_PROVINCE.keys())
        p = p[0] if p else ''

        temp.update({
            'num': num,
            'sight_id': x.id,
            'name': x.name,
            'province': x.province_key,
            'province_name': p,
            'des': x.des,
            'code': x.code,
            'state': x.state,
            'cover': cover
        })
        data.append(temp)

    return data


def search(request):
    data = []
    sb = SightBase()

    name = request.REQUEST.get('name')

    objs = []
    if name:
        objs = sb.get_sight_by_name(name, state=None)
    else:
        objs = sb.get_all_sights(state=None)

    page_index = int(request.REQUEST.get('page_index'))

    page_objs = page.Cpt(objs, count=10, page=page_index).info

    # 格式化json
    num = 10 * (page_index - 1)
    data = format_sight(page_objs[0], num)

    return HttpResponse(
        json.dumps({'data': data, 'page_count': page_objs[4], 'total_count': page_objs[5]}),
        mimetype='application/json'
    )


def get_sight_by_id(request):

    sight_id = request.REQUEST.get('sight_id')

    sight = SightBase().get_sight_by_id(sight_id, None)

    data = {}

    if sight:
        data = format_sight([sight], 1)[0]

    return HttpResponse(json.dumps(data), mimetype='application/json')


def modify_sight(request):
    sight_id = request.REQUEST.get('sight_id')
    name = request.REQUEST.get('name')
    province = request.REQUEST.get('province')
    code = request.REQUEST.get('code')
    des = request.REQUEST.get('des')
    state = request.REQUEST.get('state', '0')
    state = True if state == "1" else False
    cover = request.REQUEST.get('cover')

    tag_img = re.compile('<img .*?src=[\"\'](.+?)[\"\']')
    imgs = tag_img.findall(cover)

    flag, msg = SightBase().modify_sight(sight_id, name, province, des, code, state, imgs)

    if flag == 0:
        url = "/admin/sight?#modify/%s" % (sight_id)
    else:
        url = "/admin/sight?%s#modify/%s" % (msg, sight_id)

    return HttpResponseRedirect(url)
