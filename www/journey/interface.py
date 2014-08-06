# -*- coding: utf-8 -*-

import datetime
from django.db import transaction
from django.db.models import F

from common import utils, debug, cache
from www.misc.decorators import cache_required
from www.misc import consts
from www.message.interface import UnreadCountBase
from www.account.interface import UserBase
from www.account.interface import UserCountBase
from www.journey.models import Journey, Like


dict_err = {
    20100: u'标题过于简单，稍微详述一下',
    20101: u'标题过于冗长，稍微提炼一下',
    20102: u'内容过于简单，稍微详述一下',
    20103: u'内容过于冗长，稍微提炼一下',
    20104: u'喜欢一次足矣',
    20105: u'自己赞自己是自恋的表现哦，暂不支持',

    20800: u'问题不存在或者已删除',
    20801: u'回答不存在或者已删除',
    20802: u'绝对不会让你得逞的，因为你没得权限',
}
dict_err.update(consts.G_DICT_ERROR)

JOURNEY_DB = 'default'


def journey_required(func):
    def _decorator(self, journey_id_or_object, *args, **kwargs):
        journey = journey_id_or_object
        if not isinstance(journey_id_or_object, Journey):
            try:
                journey = Journey.objects.get(id=journey_id_or_object, state=True)
            except Journey.DoesNotExist:
                return 20800, dict_err.get(20800)
        return func(self, journey, *args, **kwargs)
    return _decorator


def journey_admin_required(func):
    def _decorator(self, journey, user, *args, **kwargs):
        flag, journey = JourneyBase().get_journey_admin_permission(journey, user)
        if not flag:
            return 20802, dict_err.get(20802)
        return func(self, journey, user, *args, **kwargs)
    return _decorator


class JourneyBase(object):

    def __init__(self):
        pass

    def format_journeys(self, journeys):
        for journey in journeys:
            journey.user = journey.get_user()
            journey.content = utils.filter_script(journey.content)
        return journeys

    def validate_title(self, title):
        if len(title) < 10:
            return 20100, dict_err.get(20100)
        if len(title) > 128:
            return 20101, dict_err.get(20101)
        return 0, dict_err.get(0)

    def validate_content(self, content, min_len=10):
        if len(content) < min_len:
            return 20102, dict_err.get(20102)
        if len(content) > 65535:
            return 20103, dict_err.get(20103)
        return 0, dict_err.get(0)

    def validata_journey_element(self, journey_title, journey_content):
        errcode, errmsg = self.validate_title(journey_title)
        if not errcode == 0:
            return errcode, errmsg

        errcode, errmsg = self.validate_content(journey_content, min_len=2)
        if not errcode == 0:
            return errcode, errmsg

        if not all((journey_title, journey_content)):
            return 99800, dict_err.get(99800)

        return 0, dict_err.get(0)

    @transaction.commit_manually(using=JOURNEY_DB)
    def create_journey(self, user_id, journey_title, journey_content,
                       ip='127.0.0.1', is_hide_user=None):
        try:
            # 防止xss漏洞
            journey_title = utils.filter_script(journey_title)
            journey_content = utils.filter_script(journey_content)

            errcode, errmsg = self.validata_journey_element(journey_title, journey_content)
            if not errcode == 0:
                transaction.rollback(using=JOURNEY_DB)
                return errcode, errmsg

            is_hide_user = True if is_hide_user else False
            journey = Journey.objects.create(user_id=user_id, title=journey_title, content=journey_content,
                                             last_answer_time=datetime.datetime.now(), ip=ip,
                                             is_hide_user=is_hide_user)

            # 更新用户话题数信息
            UserCountBase().update_user_count(user_id=user_id, code='user_journey_count')

            transaction.commit(using=JOURNEY_DB)
            return 0, journey
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=JOURNEY_DB)
            return 99900, dict_err.get(99900)

    @journey_admin_required
    @transaction.commit_manually(using=JOURNEY_DB)
    def modify_journey(self, journey, user, journey_title, journey_content,
                       ip='127.0.0.1', is_hide_user=None):
        try:
            # 防止xss漏洞
            journey_title = utils.filter_script(journey_title)
            journey_content = utils.filter_script(journey_content)

            errcode, errmsg = self.validata_journey_element(journey_title, journey_content)
            if not errcode == 0:
                transaction.rollback(using=JOURNEY_DB)
                return errcode, errmsg

            journey.title = journey_title
            journey.content = journey_content
            journey.ip = ip
            if is_hide_user:
                journey.is_hide_user = True
            journey.save()

            # 更新summary
            self.get_journey_summary_by_id(journey, must_update_cache=True)

            transaction.commit(using=JOURNEY_DB)
            return 0, journey
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=JOURNEY_DB)
            return 99900, dict_err.get(99900)

    def add_journey_view_count(self, journey_id):
        '''
        @note: 更新浏览次数
        '''
        Journey.objects.filter(id=journey_id).update(views_count=F('views_count') + 1)

    @journey_admin_required
    @transaction.commit_manually(using=JOURNEY_DB)
    def remove_journey(self, journey, user):
        try:
            journey.state = False
            journey.save()

            # 更新用户话题数信息
            UserCountBase().update_user_count(user_id=journey.user_id, code='user_journey_count', operate='minus')

            transaction.commit(using=JOURNEY_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=JOURNEY_DB)
            return 99900, dict_err.get(99900)

    def get_journey_by_id(self, id, need_state=True):
        try:
            ps = dict(id=id)
            if need_state:
                ps.update(dict(state=True))
            return Journey.objects.get(**ps)
        except Journey.DoesNotExist:
            return None

    def get_journeys_by_user_id(self, user_id):
        return Journey.objects.filter(user_id=user_id, state=True)

    def get_user_journey_count(self, user_id):
        return self.get_journeys_by_user_id(user_id).count()

    def get_all_journeys_for_home_page(self):
        return Journey.objects.filter(is_silence=False, state=True)

    def get_all_important_journey(self):
        pass

    @journey_required
    def get_journey_admin_permission(self, journey, user):
        # 返回journey值用于journey对象赋值
        return journey.user_id == user.id or user.is_staff(), journey

    @journey_required
    @transaction.commit_manually(using=JOURNEY_DB)
    def set_important(self, journey, user, title, summary, author_user_id=None, img='', img_alt=None, sort_num=0):
        try:
            if author_user_id and not UserBase().get_user_by_id(author_user_id):
                transaction.rollback(using=JOURNEY_DB)
                return 99600, dict_err.get(99600)

            try:
                assert journey and user and title and summary
            except:
                transaction.rollback(using=JOURNEY_DB)
                return 99800, dict_err.get(99800)

            journey.is_important = True
            journey.save()

            transaction.commit(using=JOURNEY_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=JOURNEY_DB)
            return 99900, dict_err.get(99900)

    @journey_required
    @transaction.commit_manually(using=JOURNEY_DB)
    def cancel_important(self, journey, user):
        try:
            journey.is_important = False
            journey.save()

            transaction.commit(using=JOURNEY_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=JOURNEY_DB)
            return 99900, dict_err.get(99900)

    @cache_required(cache_key='journey_summary_%s', expire=3600)
    def get_journey_summary_by_id(self, journey_id_or_object, must_update_cache=False):
        '''
        @note: 获取提问摘要信息，用于feed展现
        '''
        journey = self.get_journey_by_id(journey_id_or_object, need_state=False) if not isinstance(journey_id_or_object, Journey) else journey_id_or_object
        journey_summary = {}
        if journey:
            journey_summary = dict(journey_id=journey.id, journey_title=journey.title,
                                   journey_summary=journey.get_summary(), journey_answer_count=journey.answer_count)
        return journey_summary

    def get_journey_by_title(self, title):
        '''
        根据标题查询提问
        '''
        journeys = []
        if title:
            journeys = Journey.objects.filter(title=title)

        return self.format_journeys(journeys)

    def get_all_journeys_by_order_type(self, order):
        '''
        根据统计数据排序
        '''
        return self.format_journeys(Journey.objects.all().order_by('-' + order))

    def get_journeys_by_range_date(self, start_date, end_date):
        '''
        查询指定区间的提问
        '''
        return Journey.objects.filter(create_time__range=(start_date, end_date))

    def search_journeys(self, title):
        if not title:
            return []
        return Journey.objects.filter(title__icontains=title, state=True)[:200]

    def search_user_journeys(self, user_id, title):
        if not title:
            return []
        return Journey.objects.filter(user_id=user_id, title__icontains=title, state=True)[:200]


class LikeBase(object):

    '''
    @note: “喜欢”模块封装
    '''

    def format_likes(self, likes):
        for like in likes:
            like.from_user = UserBase().get_user_by_id(like.from_user_id)
        return likes

    @journey_required
    @transaction.commit_manually(JOURNEY_DB)
    def like_it(self, journey, from_user_id, ip):
        '''
        @note: 喜欢操作封装
        '''
        try:
            assert all((journey, from_user_id, ip))
            is_anonymous = False
            if from_user_id:
                if Like.objects.filter(from_user_id=from_user_id, journey=journey):
                    transaction.rollback(JOURNEY_DB)
                    return 20104, dict_err.get(20104)
            else:
                from_user_id = ''
                is_anonymous = False
                if Like.objects.filter(ip=ip, journey=journey):
                    transaction.rollback(JOURNEY_DB)
                    return 20104, dict_err.get(20104)

            # 不支持自赞
            to_user_id = journey.user_id
            if from_user_id == to_user_id:
                transaction.rollback(JOURNEY_DB)
                return 20105, dict_err.get(20105)

            Like.objects.create(journey=journey, is_anonymous=is_anonymous, from_user_id=from_user_id, to_user_id=to_user_id, ip=ip)
            journey.like_count += 1
            journey.save()

            # 更新被赞次数
            UserCountBase().update_user_count(user_id=to_user_id, code='user_liked_count')

            # 更新未读消息
            UnreadCountBase().update_unread_count(to_user_id, code='received_like')

            # 更新summary
            JourneyBase().get_journey_summary_by_id(journey, must_update_cache=True)

            transaction.commit(JOURNEY_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(JOURNEY_DB)
            return 99900, dict_err.get(99900)

    def get_likes_by_journey(self, journey, user_id=None, ip=None):
        '''
        @note: 获取某个提问下的问题的所有喜欢，用于前端判断当前登录用户是否喜欢了该回答，匿名用户采用ip判断
        '''
        ps = dict(journey=journey)
        if user_id:
            ps.update(dict(from_user_id=user_id))
        if ip:
            ps.update(dict(ip=ip, is_anonymous=True))
        return Like.objects.filter(**ps)

    def get_to_user_likes(self, user_id):
        return Like.objects.select_related('journey').filter(to_user_id=user_id, is_anonymous=False)

    def get_likes_by_answer(self, answer):
        return Like.objects.select_related('answer').filter(answer=answer, is_anonymous=False)

    def get_user_liked_count(self, user_id):
        return self.get_to_user_likes(user_id).count()
