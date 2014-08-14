# -*- coding: utf-8 -*-

import datetime
from django.db import transaction
from django.db.models import F

from common import utils, debug, cache
from www.misc.decorators import cache_required
from www.misc import consts
from www.tasks import async_send_email
from www.message.interface import UnreadCountBase
from www.account.interface import UserBase, UserCountBase
from www.journey.interface import JourneyBase
from www.answer.models import Answer, AtAnswer


dict_err = {
    20100: u'标题过于简单，稍微详述一下',
    20101: u'标题过于冗长，稍微提炼一下',
    20102: u'内容过于简单，稍微详述一下',
    20103: u'内容过于冗长，稍微提炼一下',

    40800: u'对象不存在或者已删除',
    40801: u'回答不存在或者已删除',
    40802: u'绝对不会让你得逞的，因为你没得权限',
}
dict_err.update(consts.G_DICT_ERROR)

ANSWER_DB = 'default'


def obj_required(func):
    def _decorator(self, obj_id_or_object, obj_type, *args, **kwargs):
        obj = obj_id_or_object
        if isinstance(obj_id_or_object, (int, long, str, unicode)):
            try:
                obj = AnswerBase().get_obj(obj_id_or_object, obj_type)
            except:
                return 40800, dict_err.get(40800)
        return func(self, obj, obj_type, *args, **kwargs)
    return _decorator


def answer_required(func):
    def _decorator(self, answer_id_or_object, *args, **kwargs):
        answer = answer_id_or_object
        if not isinstance(answer_id_or_object, Answer):
            try:
                answer = Answer.objects.get(id=answer_id_or_object, state=True)
            except Answer.DoesNotExist:
                return 40801, dict_err.get(40801)
        return func(self, answer, *args, **kwargs)
    return _decorator


def answer_admin_required(func):
    def _decorator(self, answer, user, *args, **kwargs):
        flag, answer = AnswerBase().get_answer_admin_permission(answer, user)
        if not flag:
            return 40802, dict_err.get(40802)
        return func(self, answer, user, *args, **kwargs)
    return _decorator


class AnswerBase(object):

    def format_answers(self, answers, need_obj=False):
        for answer in answers:
            answer.from_user = answer.get_from_user()
            answer.to_user = answer.get_to_user()
            answer.content = utils.replace_at_html(answer.content)
            if need_obj:
                answer.obj = self.get_obj(answer.obj_id, answer.obj_type)
        return answers

    def get_obj(self, obj_id, obj_type):
        from www.journey.models import Journey
        from www.activity.models import Activity

        obj_type = str(obj_type)
        try:
            if obj_type == "0":
                return Journey.objects.get(id=obj_id)
            elif obj_type == "1":
                return Activity.objects.get(id=obj_id)
            else:
                pass
        except Journey.DoesNotExist, Activity.objects.DoesNotExist:
            pass
        raise Exception, u"obj does not exist"

    @obj_required
    @transaction.commit_manually(using=ANSWER_DB)
    def create_answer(self, obj, obj_type, from_user_id, content, ip=None):
        try:
            obj_type = str(obj_type)

            content = utils.filter_script(content)
            if not all((obj, obj_type, from_user_id, content)):
                transaction.rollback(using=ANSWER_DB)
                return 99800, dict_err.get(99800)

            errcode, errmsg = JourneyBase().validate_content(content)
            if not errcode == 0:
                transaction.rollback(using=ANSWER_DB)
                return errcode, errmsg

            to_user_id = obj.user_id
            answer = Answer.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, content=content,
                                           obj_id=obj.id, obj_type=obj_type, ip=ip)

            from_user = UserBase().get_user_by_id(from_user_id)
            # 添加at信息
            if content.find('@') != -1:
                at_usernicks = utils.select_at(content)
                for nick in at_usernicks:
                    at_user = UserBase().get_user_by_nick(nick)
                    if at_user:
                        # 自己@自己的关系不进行存储
                        if at_user.id != from_user_id:
                            AtAnswer.objects.create(answer=answer, user_id=at_user.id)
                            if at_user.id != to_user_id:
                                # 更新@未读消息数
                                UnreadCountBase().update_unread_count(at_user.id, code='at_answer')

                                # 发送提醒邮件
                                context = dict(user=from_user, answer=answer)
                                # async_send_email(at_user.email, u'%s 在且行回答中@了你' % (from_user.nick, ), utils.render_email_template('email/at.html', context), 'html')

            # 更新未读消息
            if from_user_id != to_user_id:
                UnreadCountBase().update_unread_count(to_user_id, code='received_answer')

                # 发送提醒邮件
                to_user = UserBase().get_user_by_id(to_user_id)
                context = dict(user=from_user, answer=answer)
                # async_send_email(to_user.email, u'%s 在且行回答了你的提问' % (from_user.nick, ), utils.render_email_template('email/answer.html', context), 'html')

            # 更新用户回答统计总数
            UserCountBase().update_user_count(user_id=from_user_id, code='user_answer_count')

            # 更新回答数冗余信息
            obj.answer_count += 1
            obj.last_answer_time = datetime.datetime.now()
            obj.save()

            transaction.commit(using=ANSWER_DB)
            return 0, answer
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=ANSWER_DB)
            return 99900, dict_err.get(99900)

    @answer_admin_required
    def modify_answer(self, answer, user, content):
        try:
            content = utils.filter_script(content)
            if not content:
                return 99800, dict_err.get(99800)

            errcode, errmsg = JourneyBase().validate_content(content)
            if not errcode == 0:
                return errcode, errmsg

            answer.content = content
            answer.save()

            # 更新summary
            self.get_answer_summary_by_id(answer, must_update_cache=True)

            return 0, answer
        except Exception, e:
            debug.get_debug_detail(e)
            return 99900, dict_err.get(99900)

    def get_answers_by_obj_id(self, obj_id, obj_type):
        return Answer.objects.filter(obj_id=obj_id, obj_type=obj_type, state=True)

    def get_user_received_answer(self, user_id):
        return Answer.objects.filter(to_user_id=user_id, state=True)\
            .exclude(from_user_id=user_id).order_by('-id')

    def get_user_sended_answer(self, user_id):
        return Answer.objects.filter(from_user_id=user_id, state=True).order_by('-id')

    def get_at_answers(self, user_id):
        return [aa.answer for aa in AtAnswer.objects.select_related('answer').filter(user_id=user_id)]

    @answer_required
    def get_answer_admin_permission(self, answer, user):
        # 返回answer值用于answer对象赋值
        return answer.from_user_id == user.id or answer.to_user_id == user.id or user.is_staff(), answer

    @answer_admin_required
    @transaction.commit_manually(using=ANSWER_DB)
    def remove_answer(self, answer, user):
        try:
            answer.state = False
            answer.save()

            AtAnswer.objects.filter(user_id=user.id).delete()

            # 更新用户回答统计总数
            UserCountBase().update_user_count(user_id=answer.from_user_id, code='user_answer_count', operate='minus')

            # 更新回答数冗余信息
            obj = self.get_obj(answer.obj_id, answer.obj_type)
            obj.answer_count -= 1
            obj.save()

            transaction.commit(using=ANSWER_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=ANSWER_DB)
            return 99900, dict_err.get(99900)

    def get_answer_by_id(self, id, need_state=True):
        try:
            ps = dict(id=id)
            if need_state:
                ps.update(dict(state=True))
            return Answer.objects.get(**ps)
        except Answer.DoesNotExist:
            return None

    @cache_required(cache_key='answer_summary_%s', expire=3600)
    def get_answer_summary_by_id(self, answer_id_or_object, must_update_cache=False):
        '''
        @note: 获取回答摘要信息，用于feed展现
        '''
        answer = self.get_answer_by_id(answer_id_or_object, need_state=False) if not isinstance(answer_id_or_object, Answer) else answer_id_or_object
        answer_summary = {}
        if answer:
            user = answer.get_from_user()
            obj = self.get_obj(answer.obj_id, answer.obj_type)
            answer_summary = dict(answer_id=answer.id, obj_id=answer.obj_id, obj_title=obj.title,
                                  answer_summary=answer.get_summary(), answer_like_count=answer.like_count, answer_user_id=user.id,
                                  answer_user_avatar=user.get_avatar_65(), answer_user_nick=user.nick, answer_user_des=user.des or '')
        return answer_summary

    def get_answers_by_range_date(self, start_date, end_date):
        '''
        查询指定区间的回答
        '''
        return Answer.objects.filter(create_time__range=(start_date, end_date))

    def search_answers(self, content):
        if not content:
            return []
        return Answer.objects.filter(content__icontains=content, state=True)[:200]

    def search_user_answers(self, user_id, content):
        if not content:
            return []
        return Answer.objects.filter(from_user_id=user_id, content__icontains=content, state=True)[:200]
