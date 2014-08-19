# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from www.misc.decorators import staff_required, common_ajax_response, verify_permission
from www.misc import qiniu_client
from common import utils, page

from www.admin.interface import CoverBase


@verify_permission('')
def home_cover(request, template_name='admin/home_cover.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def format_cover(objs, num):
    data = []

    for x in objs:
        num += 1

        data.append({
            'num': num,
            'cover_id': x.id,
            'des': x.des,
            'img': x.img,
            'link': x.link,
            'sort': x.sort_num
        })

    return data


@verify_permission('query_home_cover')
def search(request):

    data = CoverBase().get_home_cover()

    return HttpResponse(
        json.dumps({'data': format_cover(data, 0)}),
        mimetype='application/json'
    )


@verify_permission('add_home_cover')
def add_cover(request):

    sort = request.REQUEST.get('sort')
    link = request.REQUEST.get('link')
    des = request.REQUEST.get('des')

    img = request.FILES.get('img')
    img_name = None
    if img:
        flag, img_name = qiniu_client.upload_img(img, img_type='topic')
        img_name = '%s/%s' % (settings.IMG0_DOMAIN, img_name)

    flag, msg = CoverBase().add_cover(img_name, link, sort, des)

    if flag == 0:
        url = "/admin/home_cover?#modify/%s" % (msg)
    else:
        url = "/admin/home_cover?%s" % (msg)

    return HttpResponseRedirect(url)


@verify_permission('query_home_cover')
def get_cover_by_id(request):
    cover_id = request.REQUEST.get('cover_id')

    obj = CoverBase().get_cover_by_id(cover_id)

    return HttpResponse(
        json.dumps(format_cover([obj], 0)[0]),
        mimetype='application/json'
    )


@verify_permission('modify_home_cover')
def modify_cover(request):

    cover_id = request.REQUEST.get('cover_id')
    sort = request.REQUEST.get('sort')
    link = request.REQUEST.get('link')
    des = request.REQUEST.get('des')

    img = request.FILES.get('img')
    img_name = None
    if img:
        flag, img_name = qiniu_client.upload_img(img, img_type='topic')
        img_name = '%s/%s' % (settings.IMG0_DOMAIN, img_name)

    flag, msg = CoverBase().modify_cover(cover_id, img_name, link, sort, des)

    if flag == 0:
        url = "/admin/home_cover?#modify/%s" % (cover_id)
    else:
        url = "/admin/home_cover?%s#modify/%s" % (msg, cover_id)

    return HttpResponseRedirect(url)


@verify_permission('remove_home_cover')
@common_ajax_response
def remove_cover(request):
    cover_id = request.REQUEST.get('cover_id')

    return CoverBase().remove_cover(cover_id)
