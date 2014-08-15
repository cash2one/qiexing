# -*- coding: utf-8 -*-

import datetime
from django.db import transaction
# from django.db.models import F

from common import utils, debug
from www.misc.decorators import cache_required
from www.misc import consts
# from www.tasks import async_send_email
# from www.message.interface import UnreadCountBase
from www.account.interface import UserBase
from www.journey.interface import JourneyBase
from www.activity.models import Activity, ActivityPerson


dict_err = {
    20100: u'标题过于简单，稍微详述一下',
    20101: u'标题过于冗长，稍微提炼一下',
    20102: u'内容过于简单，稍微详述一下',
    20103: u'内容过于冗长，稍微提炼一下',

    30801: u'活动不存在或者已删除',
    30802: u'绝对不会让你得逞的，因为你没得权限',
    30803: u'活动结束时间不能早于开始时间',
    30804: u'活动开始时间不能早于当前时间',
    30805: u'报名截止时间不能早于当前时间',
    30806: u'已经报名了该活动',
    30807: u'该用户未报名',
}
dict_err.update(consts.G_DICT_ERROR)

ACTIVITY_DB = 'default'


def activity_required(func):
    def _decorator(self, activity_id_or_object, *args, **kwargs):
        activity = activity_id_or_object
        if not isinstance(activity_id_or_object, Activity):
            try:
                activity = Activity.objects.get(id=activity_id_or_object, state=True)
            except Activity.DoesNotExist:
                return 30801, dict_err.get(30801)
        return func(self, activity, *args, **kwargs)
    return _decorator


def activity_admin_required(func):
    def _decorator(self, activity, user, *args, **kwargs):
        flag, activity = ActivityBase().get_activity_admin_permission(activity, user)
        if not flag:
            return 30802, dict_err.get(30802)
        return func(self, activity, user, *args, **kwargs)
    return _decorator


class ActivityBase(object):

    def format_activitys(self, activitys, request_user=None):
        for activity in activitys:
            activity.user = activity.get_user()
            if request_user:
                activity.is_user_in = ActivityPersonBase().is_user_in_activity(activity, request_user.id)
        return activitys

    def get_activity_by_id(self, id, need_state=True):
        try:
            ps = dict(id=id)
            if need_state:
                ps.update(dict(state=True))
            return Activity.objects.get(**ps)
        except Activity.DoesNotExist:
            return None

    def get_all_valid_activitys(self):
        return Activity.objects.filter(state=True)

    def check_date(self, start_date, end_date, sign_up_end_date):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        sign_up_end_date = datetime.datetime.strptime(sign_up_end_date, "%Y-%m-%d").date()
        now = datetime.datetime.now()
        if start_date > end_date:
            return 30803, dict_err.get(30803)
        if start_date < now.date():
            return 30804, dict_err.get(30804)
        if sign_up_end_date < now.date():
            return 30805, dict_err.get(30805)
        return 0, dict_err.get(0)

    @transaction.commit_manually(using=ACTIVITY_DB)
    def create_activity(self, user_id, title, content, start_date, end_date, sign_up_end_date, addr, assembly_point, activity_cover):
        try:

            content = utils.filter_script(content)
            if not all((user_id, title, content, start_date, end_date, sign_up_end_date, activity_cover, addr, assembly_point)):
                transaction.rollback(using=ACTIVITY_DB)
                return 99800, dict_err.get(99800)

            errcode, errmsg = JourneyBase().validate_journey_element(title, content, min_title_len=5)
            if not errcode == 0:
                transaction.rollback(using=ACTIVITY_DB)
                return errcode, errmsg

            # 检测时间是否正常
            errcode, errmsg = self.check_date(start_date, end_date, sign_up_end_date)
            if not errcode == 0:
                transaction.rollback(using=ACTIVITY_DB)
                return errcode, errmsg

            activity = Activity.objects.create(user_id=user_id, title=title, content=content, start_date=start_date, end_date=end_date,
                                               sign_up_end_date=sign_up_end_date, activity_cover=activity_cover, addr=addr, assembly_point=assembly_point)

            transaction.commit(using=ACTIVITY_DB)
            return 0, activity
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=ACTIVITY_DB)
            return 99900, dict_err.get(99900)

    @activity_admin_required
    @transaction.commit_manually(using=ACTIVITY_DB)
    def modify_activity(self, activity, user, title, content, start_date, end_date, sign_up_end_date, addr, assembly_point, activity_cover=None):
        try:
            content = utils.filter_script(content)
            if not all((title, content, start_date, end_date, sign_up_end_date, addr, assembly_point)):
                transaction.rollback(using=ACTIVITY_DB)
                return 99800, dict_err.get(99800)

            errcode, errmsg = JourneyBase().validate_journey_element(title, content, min_title_len=5)
            if not errcode == 0:
                return errcode, errmsg

            # 检测时间是否正常
            errcode, errmsg = self.check_date(start_date, end_date, sign_up_end_date)
            if not errcode == 0:
                transaction.rollback(using=ACTIVITY_DB)
                return errcode, errmsg

            activity.title = title
            activity.content = content
            activity.start_date = start_date
            activity.end_date = end_date
            activity.sign_up_end_date = sign_up_end_date
            if activity_cover:
                activity.activity_cover = activity_cover
            activity.addr = addr
            activity.assembly_point = assembly_point
            activity.save()

            # 更新summary
            self.get_activity_summary_by_id(activity, must_update_cache=True)
            transaction.commit(using=ACTIVITY_DB)
            return 0, activity
        except Exception, e:
            transaction.rollback(using=ACTIVITY_DB)
            debug.get_debug_detail(e)
            return 99900, dict_err.get(99900)

    @activity_required
    def get_activity_admin_permission(self, activity, user):
        # 返回activity值用于activity对象赋值
        return activity.user_id == user.id or user.is_staff(), activity

    @activity_admin_required
    @transaction.commit_manually(using=ACTIVITY_DB)
    def remove_activity(self, activity, user):
        try:
            activity.state = False
            activity.save()

            transaction.commit(using=ACTIVITY_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=ACTIVITY_DB)
            return 99900, dict_err.get(99900)

    @cache_required(cache_key='activity_summary_%s', expire=3600)
    def get_activity_summary_by_id(self, activity_id_or_object, must_update_cache=False):
        '''
        @note: 获取回答摘要信息，用于feed展现
        '''
        activity = self.get_activity_by_id(activity_id_or_object, need_state=False) if not isinstance(activity_id_or_object, Activity) else activity_id_or_object
        activity_summary = {}
        if activity:
            user = activity.get_user()
            activity_summary = dict(activity_id=activity.id, activity_title=activity.title,
                                    activity_summary=activity.get_summary(), activity_user_id=user.id,
                                    activity_user_avatar=user.get_avatar_65(), activity_user_nick=user.nick, activity_user_des=user.des or '')
        return activity_summary


class ActivityPersonBase(object):

    def __init__(self):
        pass

    def format_activity_persons(self, activity_persons):
        for activity_person in activity_persons:
            activity_person.user = UserBase().get_user_by_id(activity_person.user_id)
        return activity_persons

    def get_activity_persons_by_activity(self, activity):
        return ActivityPerson.objects.filter(activity=activity, state=1)

    @activity_required
    @transaction.commit_manually(using=ACTIVITY_DB)
    def join_activity(self, activity, user_id, real_name, mobile, partner_count, state=0):
        try:
            if not all((user_id, real_name, mobile)):
                transaction.rollback(using=ACTIVITY_DB)
                return 99800, dict_err.get(99800)

            if ActivityPerson.objects.filter(activity=activity, user_id=user_id):
                transaction.rollback(using=ACTIVITY_DB)
                return 30806, dict_err.get(30806)

            ActivityPerson.objects.create(activity=activity, user_id=user_id, real_name=real_name, mobile=mobile,
                                          partner_count=partner_count, state=state)

            if state > 0:
                activity.person_count += 1
                activity.save()

            transaction.commit(using=ACTIVITY_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=ACTIVITY_DB)
            return 99900, dict_err.get(99900)

    @activity_required
    @transaction.commit_manually(using=ACTIVITY_DB)
    def set_join_state(self, activity, request_user, activity_person_key_id, state):
        try:
            try:
                ap = ActivityPerson.objects.get(id=activity_person_key_id)
            except ActivityPerson.DoesNotExist:
                transaction.rollback(using=ACTIVITY_DB)
                return 30807, dict_err.get(30807)

            if state == 1 and ap.state == 0:
                activity.person_count += 1
                activity.save()
            if state == 0 and ap.state == 1:
                activity.person_count -= 1
                activity.save()

            ap.state = state
            ap.save()

            transaction.commit(using=ACTIVITY_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=ACTIVITY_DB)
            return 99900, dict_err.get(99900)

    def is_user_in_activity(self, activity, user_id):
        return True if ActivityPerson.objects.filter(activity=activity, user_id=user_id) else False
