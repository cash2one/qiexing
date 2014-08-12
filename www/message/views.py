# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse  # , HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page
from www.misc.decorators import member_required
from www.tasks import async_clear_count_info_by_code
from www.account import interface as interface_account
from www.journey import interface as interface_journey
from www.answer import interface as interface_answer
from www.message import interface


urb = interface.UnreadCountBase()
lb = interface_journey.LikeBase()
ab = interface_answer.AnswerBase()
ub = interface_account.UserBase()


@member_required
def system_message(request, template_name='message/system_message.html'):
    # system_messages = urb.get_system_message(request.user.id)

    # 分页
    # page_num = int(request.REQUEST.get('page', 1))
    # page_objs = page.Cpt(system_messages, count=10, page=page_num).info
    # system_messages = page_objs[0]
    # page_params = (page_objs[1], page_objs[4])

    # 异步清除未读消息数
    # async_clear_count_info_by_code(request.user.id, code='system_message')
    # unread_count_info = urb.get_unread_count_info(request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def received_like(request, template_name='message/received_like.html'):

    # likes = lb.get_to_user_likes(request.user.id)

    # 分页
    # page_num = int(request.REQUEST.get('page', 1))
    # page_objs = page.Cpt(likes, count=10, page=page_num).info
    # likes = page_objs[0]
    # page_params = (page_objs[1], page_objs[4])
    # likes = lb.format_likes(likes)
    # likes_count = page_objs[5]

    # 异步清除未读消息数
    # async_clear_count_info_by_code(request.user.id, code='received_like')
    # unread_count_info = urb.get_unread_count_info(request.user)

    # user_agent_dict = user_agent_parser.Parse(request.META.get('HTTP_USER_AGENT'))

    # 手机客户端换模板
    # if user_agent_dict['os']['family'] in ('Android', 'iOS'):
    #     template_name = 'message/received_like_m.html'

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def received_answer(request, template_name='message/received_answer.html'):
    # answers = ab.get_user_received_answer(request.user.id)

    # 分页
    # page_num = int(request.REQUEST.get('page', 1))
    # page_objs = page.Cpt(answers, count=10, page=page_num).info
    # answers = page_objs[0]
    # page_params = (page_objs[1], page_objs[4])
    # answers = ab.format_answers(answers)

    # 异步清除未读消息数
    # async_clear_count_info_by_code(request.user.id, code='received_answer')
    # unread_count_info = urb.get_unread_count_info(request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def at_answer(request, template_name='message/at_answer.html'):
    # answers = ab.get_at_answers(request.user.id)

    # 分页
    # page_num = int(request.REQUEST.get('page', 1))
    # page_objs = page.Cpt(answers, count=10, page=page_num).info
    # answers = page_objs[0]
    # page_params = (page_objs[1], page_objs[4])
    # answers = ab.format_answers(answers)

    # 异步清除未读消息数
    # async_clear_count_info_by_code(request.user.id, code='at_answer')
    # unread_count_info = urb.get_unread_count_info(request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# ===================================================ajax部分=================================================================#
@member_required
def get_unread_count_total(request):
    count_info = urb.get_unread_count_total(request.user)

    # 更新最后活跃时间
    ub.update_user_last_active_time(request.user.id, ip=utils.get_clientip(request))
    return HttpResponse(json.dumps(count_info), mimetype='application/json')


@member_required
def get_all_valid_global_notice(request):
    gnb = interface.GlobalNoticeBase()
    global_notice = gnb.format_global_notice(gnb.get_all_valid_global_notice())
    return HttpResponse(json.dumps(global_notice), mimetype='application/json')
