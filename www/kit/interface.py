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
from www.kit.models import Kit


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

KIT_DB = 'default'


def kit_required(func):
    def _decorator(self, kit_id_or_object, *args, **kwargs):
        kit = kit_id_or_object
        if not isinstance(kit_id_or_object, Kit):
            try:
                kit = Kit.objects.get(id=kit_id_or_object, state=True)
            except Kit.DoesNotExist:
                return 20800, dict_err.get(20800)
        return func(self, kit, *args, **kwargs)
    return _decorator


def kit_admin_required(func):
    def _decorator(self, kit, user, *args, **kwargs):
        flag, kit = KitBase().get_kit_admin_permission(kit, user)
        if not flag:
            return 20802, dict_err.get(20802)
        return func(self, kit, user, *args, **kwargs)
    return _decorator


class KitBase(object):

    def __init__(self):
        pass

    def format_kits(self, kits):
        for kit in kits:
            kit.user = kit.get_user()
            kit.content = utils.filter_script(kit.content)
        return kits

    def validate_title(self, title, min_len=10):
        if len(title) < min_len:
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

    def validate_kit_element(self, kit_title, kit_content, min_title_len=10):
        errcode, errmsg = self.validate_title(kit_title, min_title_len)
        if not errcode == 0:
            return errcode, errmsg

        errcode, errmsg = self.validate_content(kit_content, min_len=2)
        if not errcode == 0:
            return errcode, errmsg

        if not all((kit_title, kit_content)):
            return 99800, dict_err.get(99800)

        return 0, dict_err.get(0)

    @transaction.commit_manually(using=KIT_DB)
    def create_kit(self, user_id, kit_title, kit_content,
                       ip='127.0.0.1', is_hide_user=None):
        try:
            # 防止xss漏洞
            kit_title = utils.filter_script(kit_title)
            kit_content = utils.filter_script(kit_content)

            errcode, errmsg = self.validate_kit_element(kit_title, kit_content)
            if not errcode == 0:
                transaction.rollback(using=KIT_DB)
                return errcode, errmsg

            is_hide_user = True if is_hide_user else False
            kit = Kit.objects.create(user_id=user_id, title=kit_title, content=kit_content,
                                             last_answer_time=datetime.datetime.now(), ip=ip,
                                             is_hide_user=is_hide_user)

            # 更新用户话题数信息
            # UserCountBase().update_user_count(user_id=user_id, code='user_kit_count')

            transaction.commit(using=KIT_DB)
            return 0, kit
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=KIT_DB)
            return 99900, dict_err.get(99900)

    @kit_admin_required
    @transaction.commit_manually(using=KIT_DB)
    def modify_kit(self, kit, user, kit_title, kit_content,
                       ip='127.0.0.1', is_hide_user=None):
        try:
            # 防止xss漏洞
            kit_title = utils.filter_script(kit_title)
            kit_content = utils.filter_script(kit_content)

            errcode, errmsg = self.validate_kit_element(kit_title, kit_content)
            if not errcode == 0:
                transaction.rollback(using=KIT_DB)
                return errcode, errmsg

            kit.title = kit_title
            kit.content = kit_content
            kit.ip = ip
            if is_hide_user:
                kit.is_hide_user = True
            kit.save()

            # 更新summary
            self.get_kit_summary_by_id(kit, must_update_cache=True)

            transaction.commit(using=KIT_DB)
            return 0, kit
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=KIT_DB)
            return 99900, dict_err.get(99900)

    def add_kit_view_count(self, kit_id):
        '''
        @note: 更新浏览次数
        '''
        Kit.objects.filter(id=kit_id).update(views_count=F('views_count') + 1)

    @kit_admin_required
    @transaction.commit_manually(using=KIT_DB)
    def remove_kit(self, kit, user):
        try:
            kit.state = False
            kit.save()

            # 更新用户话题数信息
            # UserCountBase().update_user_count(user_id=kit.user_id, code='user_kit_count', operate='minus')

            transaction.commit(using=KIT_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=KIT_DB)
            return 99900, dict_err.get(99900)

    def get_kit_by_id(self, id, need_state=True):
        try:
            ps = dict(id=id)
            if need_state:
                ps.update(dict(state=True))
            return Kit.objects.get(**ps)
        except Kit.DoesNotExist:
            return None

    def get_kits_by_user_id(self, user_id):
        return Kit.objects.filter(user_id=user_id, state=True)

    def get_user_kit_count(self, user_id):
        return self.get_kits_by_user_id(user_id).count()

    def get_all_kits_for_home_page(self):
        return Kit.objects.filter(is_silence=False, state=True)

    def get_all_important_kit(self):
        pass

    @kit_required
    def get_kit_admin_permission(self, kit, user):
        # 返回kit值用于kit对象赋值
        return kit.user_id == user.id or user.is_staff(), kit

    @kit_required
    @transaction.commit_manually(using=KIT_DB)
    def set_important(self, kit, user, title, summary, author_user_id=None, img='', img_alt=None, sort_num=0):
        try:
            if author_user_id and not UserBase().get_user_by_id(author_user_id):
                transaction.rollback(using=KIT_DB)
                return 99600, dict_err.get(99600)

            try:
                assert kit and user and title and summary
            except:
                transaction.rollback(using=KIT_DB)
                return 99800, dict_err.get(99800)

            kit.is_important = True
            kit.save()

            transaction.commit(using=KIT_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=KIT_DB)
            return 99900, dict_err.get(99900)

    @kit_required
    @transaction.commit_manually(using=KIT_DB)
    def cancel_important(self, kit, user):
        try:
            kit.is_important = False
            kit.save()

            transaction.commit(using=KIT_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=KIT_DB)
            return 99900, dict_err.get(99900)

    @cache_required(cache_key='kit_summary_%s', expire=3600)
    def get_kit_summary_by_id(self, kit_id_or_object, must_update_cache=False):
        '''
        @note: 获取提问摘要信息，用于feed展现
        '''
        kit = self.get_kit_by_id(kit_id_or_object, need_state=False) if not isinstance(kit_id_or_object, Kit) else kit_id_or_object
        kit_summary = {}
        if kit:
            kit_summary = dict(kit_id=kit.id, kit_title=kit.title,
                                   kit_summary=kit.get_summary(), kit_answer_count=kit.answer_count)
        return kit_summary

    def get_kit_by_title(self, title):
        '''
        根据标题查询提问
        '''
        kits = []
        if title:
            kits = Kit.objects.filter(title=title)

        return self.format_kits(kits)

    def get_all_kits_by_order_type(self, order):
        '''
        根据统计数据排序
        '''
        return self.format_kits(Kit.objects.all().order_by('-' + order))

    def get_kits_by_range_date(self, start_date, end_date):
        '''
        查询指定区间的提问
        '''
        return Kit.objects.filter(create_time__range=(start_date, end_date))

    def search_kits(self, title):
        if not title:
            return []
        return Kit.objects.filter(title__icontains=title, state=True)[:200]

    def search_user_kits(self, user_id, title):
        if not title:
            return []
        return Kit.objects.filter(user_id=user_id, title__icontains=title, state=True)[:200]

    @kit_required
    def set_top(self, kit):
        try:
            kits = Kit.objects.filter(state=True).order_by("-sort_num")
            max_sort_num = 1 if not kits else (kits[0].sort_num + 1)
            kit.sort_num = max_sort_num
            kit.save()

            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            return 99900, dict_err.get(99900)

    @kit_required
    def cancel_top(self, kit):
        kit.sort_num = 0
        kit.save()

        return 0, dict_err.get(0)