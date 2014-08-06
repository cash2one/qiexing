# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils
from www.answer import interface
from www.misc.decorators import member_required, common_ajax_response


ab = interface.AnswerBase()


@member_required
def create_answer(request):
    answer_content = request.POST.get('answer_content', '').strip()
    obj_id = request.POST.get('obj_id', '').strip()
    obj_type = request.POST.get('obj_type', '').strip()
    obj = ab.get_obj(obj_id, obj_type)

    errcode, result = ab.create_answer(obj, obj_type, request.user.id, answer_content, ip=utils.get_clientip(request))
    if errcode == 0:
        return HttpResponseRedirect(obj.get_url())
    else:
        request.session['error_msg'] = result
        request.session['answer_content'] = answer_content
        return HttpResponseRedirect(obj.get_url())


@member_required
def modify_answer(request):
    if request.POST:
        answer_id = request.POST.get('answer_id')
        edit_answer_content = request.POST.get('edit_answer_content', '').strip()

        obj_id = request.POST.get('obj_id', '').strip()
        obj_type = request.POST.get('obj_type', '').strip()
        obj = ab.get_obj(obj_id, obj_type)

        errcode, result = ab.modify_answer(answer_id, request.user, edit_answer_content)
        if errcode == 0:
            request.session['success_msg'] = u'修改成功'
            return HttpResponseRedirect(obj.get_url())
        else:
            request.session['error_msg'] = result
            return HttpResponseRedirect(obj.get_url())


@member_required
@common_ajax_response
def remove_answer(request):
    answer_id = request.POST.get('answer_id', '').strip()
    return ab.remove_answer(answer_id, request.user)
