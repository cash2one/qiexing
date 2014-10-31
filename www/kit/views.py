# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page
from www.kit import interface
from www.misc.decorators import member_required, staff_required, common_ajax_response
from www.admin.interface import CoverBase

jb = interface.KitBase()
lb = interface.LikeBase()


def kit_list(request, template_name='kit/kit_list.html'):

    kits = jb.get_all_kits_for_home_page()

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(kits, count=10, page=page_num).info
    kits = page_objs[0]
    page_params = (page_objs[1], page_objs[4])

    kits = jb.format_kits(kits)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def kit_detail(request, kit_id, template_name='kit/kit_detail.html'):
    kit = jb.get_kit_by_id(kit_id)
    if not kit:
        raise Http404
    kit = jb.format_kits([kit, ],)[0]

    sort = request.REQUEST.get('sort', 'like_count')

    answers_list_params = "%s$%s" % (kit.id, "2")  # 用于前端提取回复列表

    # 从session中获取提示信息
    if request.session.has_key('error_msg'):
        error_msg = request.session['error_msg']
        del request.session['error_msg']
    if request.session.has_key('success_msg'):
        success_msg = request.session['success_msg']
        del request.session['success_msg']
    if request.session.has_key('answer_content'):
        request.answer_content = request.session['answer_content']
        del request.session['answer_content']
    if request.session.has_key('guide'):
        guide = request.session['guide']
        del request.session['guide']

    # 异步更新浏览次数
    from www.tasks import async_add_kit_view_count
    async_add_kit_view_count(kit.id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def write_kit(request, template_name='kit/write_kit.html'):
    if request.POST:
        kit_title = request.POST.get('kit_title', '').strip()
        kit_content = request.POST.get('kit_content', '').strip()
        is_hide_user = request.POST.get('is_hide_user')

        errcode, result = jb.create_kit(request.user.id, kit_title, kit_content,
                                            ip=utils.get_clientip(request), is_hide_user=is_hide_user)
        if errcode == 0:
            request.session['guide'] = True
            return HttpResponseRedirect(result.get_url())
        else:
            error_msg = result

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def modify_kit(request, kit_id):
    if request.POST:
        kit_title = request.POST.get('kit_title', '').strip()
        kit_content = request.POST.get('kit_content', '').strip()
        is_hide_user = request.POST.get('is_hide_user')

        errcode, result = jb.modify_kit(kit_id, request.user, kit_title, kit_content,
                                            ip=utils.get_clientip(request), is_hide_user=is_hide_user)
        if errcode == 0:
            request.session['success_msg'] = u'修改成功'
            return HttpResponseRedirect(result.get_url())
        else:
            request.session['error_msg'] = result
            return HttpResponseRedirect(jb.get_kit_by_id(kit_id).get_url())


# ===================================================ajax部分=================================================================#


@member_required
@common_ajax_response
def like_kit(request):
    kit_id = request.POST.get('kit_id', '').strip()
    return lb.like_it(kit_id, request.user.id, ip=utils.get_clientip(request))


@member_required
@common_ajax_response
def remove_kit(request):
    kit_id = request.POST.get('kit_id', '').strip()
    return jb.remove_kit(kit_id, request.user)


@staff_required
@common_ajax_response
def set_top(request):
    kit_id = request.POST.get('kit_id', '').strip()
    return jb.set_top(kit_id)


@staff_required
@common_ajax_response
def cancel_top(request):
    kit_id = request.POST.get('kit_id', '').strip()
    return jb.cancel_top(kit_id)
