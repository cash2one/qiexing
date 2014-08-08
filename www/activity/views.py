# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from www.misc import qiniu_client
from www.misc.decorators import member_required, staff_required, common_ajax_response
from www.activity import interface

ab = interface.ActivityBase()


def activity_list(request, template_name='activity/activity_list.html'):
    activitys = ab.format_activitys(ab.get_all_valid_activitys())

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def activity_detail(request, activity_id=None, template_name='activity/activity_detail.html'):
    activity = ab.get_activity_by_id(activity_id)
    if not activity:
        raise Http404
    activity = ab.format_activitys([activity, ])[0]

    answers_list_params = "%s$%s" % (activity.id, "1")  # 用于前端提取回复列表

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

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@staff_required
def create_activity(request, template_name='activity/create_activity.html'):
    if request.POST:
        activity_title = request.POST.get('activity_title', '').strip()
        activity_content = request.POST.get('activity_content', '').strip()
        start_date = request.POST.get('start_date', '').strip()
        end_date = request.POST.get('end_date', '').strip()
        activity_addr = request.POST.get('activity_addr', '').strip()
        sign_up_end_date = request.POST.get('sign_up_end_date', '').strip()
        assembly_point = request.POST.get('assembly_point', '').strip()

        flag, img_name = qiniu_client.upload_img(request.FILES.get('activity_cover'), img_type='activity')
        img_name = '%s/%s' % (settings.IMG0_DOMAIN, img_name) if flag else ""

        errcode, result = ab.create_activity(request.user.id, activity_title, activity_content, start_date, end_date,
                                             sign_up_end_date, activity_addr, assembly_point, img_name)
        if errcode == 0:
            return HttpResponseRedirect(result.get_url())
        else:
            error_msg = result
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
