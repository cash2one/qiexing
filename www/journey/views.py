# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page
from www.journey import interface
from www.misc.decorators import member_required, staff_required, common_ajax_response


jb = interface.JourneyBase()
lb = interface.LikeBase()


def home(request, template_name='journey/home.html'):
    from www.activity.interface import ActivityBase
    activitys = ActivityBase().get_all_valid_activitys()[:3]
    journeys = jb.format_journeys(jb.get_all_journeys_for_home_page()[:4])

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def journey_list(request, template_name='journey/journey_list.html'):

    journeys = jb.get_all_journeys_for_home_page()

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(journeys, count=10, page=page_num).info
    journeys = page_objs[0]
    page_params = (page_objs[1], page_objs[4])

    journeys = jb.format_journeys(journeys)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def journey_detail(request, journey_id, template_name='journey/journey_detail.html'):
    journey = jb.get_journey_by_id(journey_id)
    if not journey:
        raise Http404
    journey = jb.format_journeys([journey, ],)[0]

    sort = request.REQUEST.get('sort', 'like_count')

    answers_list_params = "%s$%s" % (journey.id, "0")  # 用于前端提取回复列表

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
    from www.tasks import async_add_journey_view_count
    async_add_journey_view_count(journey.id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def write_journey(request, template_name='journey/write_journey.html'):
    if request.POST:
        journey_title = request.POST.get('journey_title', '').strip()
        journey_content = request.POST.get('journey_content', '').strip()
        is_hide_user = request.POST.get('is_hide_user')

        errcode, result = jb.create_journey(request.user.id, journey_title, journey_content,
                                            ip=utils.get_clientip(request), is_hide_user=is_hide_user)
        if errcode == 0:
            request.session['guide'] = True
            return HttpResponseRedirect(result.get_url())
        else:
            error_msg = result

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def modify_journey(request, journey_id):
    if request.POST:
        journey_title = request.POST.get('journey_title', '').strip()
        journey_content = request.POST.get('journey_content', '').strip()
        is_hide_user = request.POST.get('is_hide_user')

        errcode, result = jb.modify_journey(journey_id, request.user, journey_title, journey_content,
                                            ip=utils.get_clientip(request), is_hide_user=is_hide_user)
        if errcode == 0:
            request.session['success_msg'] = u'修改成功'
            return HttpResponseRedirect(result.get_url())
        else:
            request.session['error_msg'] = result
            return HttpResponseRedirect(jb.get_journey_by_id(journey_id).get_url())


# ===================================================ajax部分=================================================================#


@member_required
@common_ajax_response
def like_journey(request):
    journey_id = request.POST.get('journey_id', '').strip()
    return lb.like_it(journey_id, request.user.id, ip=utils.get_clientip(request))


@member_required
@common_ajax_response
def remove_journey(request):
    journey_id = request.POST.get('journey_id', '').strip()
    return jb.remove_journey(journey_id, request.user)


@staff_required
@common_ajax_response
def set_important(request):
    journey_id = request.POST.get('journey_id', '').strip()
    return jb.set_important(journey_id, request.user)


@staff_required
@common_ajax_response
def cancel_important(request):
    journey_id = request.POST.get('journey_id', '').strip()
    return jb.cancel_important(journey_id, request.user)
