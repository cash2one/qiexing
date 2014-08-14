# -*- coding: utf-8 -*-

from django.db import transaction

from www.misc import consts
from common import debug, utils
from www.sight.models import Sight, SightImg


dict_err = {
    50100: u'景点不存在或者已删除',
    50101: u'景点必须上传封面',
    50102: u'景点名称重复',
}
dict_err.update(consts.G_DICT_ERROR)


def sight_required(func):
    def _decorator(self, sight_id_or_object, *args, **kwargs):
        sight = sight_id_or_object
        if not isinstance(sight_id_or_object, Sight):
            try:
                sight = Sight.objects.get(id=sight_id_or_object, state=True)
            except Sight.DoesNotExist:
                return 50100, dict_err.get(50100)
        return func(self, sight, *args, **kwargs)
    return _decorator


class SightBase(object):

    def __init__(self):
        pass

    def format_sights(self, sights):
        for sight in sights:
            sight.imgs = self.get_sight_imgs(sight)
        return sights

    def get_province_name_by_key(self, province_key):
        for key in consts.G_PROVINCE:
            if str(consts.G_PROVINCE[key][0]) == str(province_key):
                return key
        raise Exception, u"get_province_name_by_key error"

    def get_format_sights_for_map(self):
        sights = Sight.objects.all()
        pcount = len(consts.G_PROVINCE.keys())
        format_sights = []
        for i in range(pcount):
            format_sights.append({})

        for sight in sights:
            province_name = self.get_province_name_by_key(sight.province_key)
            if "name" not in format_sights[int(sight.province_key) - 1]:
                format_sights[int(sight.province_key) - 1]["name"] = province_name
                format_sights[int(sight.province_key) - 1]["sights"] = [dict(id=sight.id, name=sight.name)]
            else:
                format_sights[int(sight.province_key) - 1]["sights"].append(dict(id=sight.id, name=sight.name))
        return format_sights

    def get_sight_by_id(self, id, state=None):
        ps = dict(id=id)
        if state is not None:
            ps.update(state=state)
        try:
            return Sight.objects.get(**ps)
        except Sight.DoesNotExist:
            pass

    def get_sight_imgs(self, sight):
        return SightImg.objects.filter(sight=sight)

    def get_province_by_name(self, name):
        from www.misc.consts import G_PROVINCE

        result = {}
        for k in G_PROVINCE.keys():
            if k.find(name) > -1:
                result[k] = G_PROVINCE[k]

        return result

    @transaction.commit_manually
    def add_sight(self, name, province, des, code=None, imgs=[]):
        if None in (name, province, des):
            return 99800, dict_err.get(99800)

        if not imgs:
            return 50101, dict_err.get(50101)

        if Sight.objects.filter(name=name):
            return 50102, dict_err.get(50102)

        sight = None
        try:
            sight = Sight.objects.create(
                name=name, code=code, province_key=province, des=des
            )

            for img in imgs:
                SightImg.objects.create(sight=sight, img=img.replace('!600m0', ''))

            transaction.commit()
        except Exception, e:
            transaction.rollback()
            debug.get_debug_detail(e)
            return 99900, dict_err.get(99900)

        return 0, sight

    def get_sight_by_name(self, name, state=None):
        ps = dict(name__contains=name)
        if state is not None:
            ps.update(state=state)
        try:
            return Sight.objects.filter(**ps)
        except Sight.DoesNotExist:
            pass

    def get_all_sights(self, state=None):
        ps = {}
        if state is not None:
            ps.update(state=state)

        return Sight.objects.filter(**ps)

    @transaction.commit_manually
    def modify_sight(self, sight_id, name, province, des, code=None, state=True, imgs=[]):
        if None in (sight_id, name, province, des):
            return 99800, dict_err.get(99800)

        if not imgs:
            return 50101, dict_err.get(50101)

        sight = self.get_sight_by_id(sight_id, None)

        if not sight:
            transaction.rollback()
            return 50100, dict_err.get(50100)

        temp = Sight.objects.filter(name=name)

        if temp and temp[0].id != sight.id:
            transaction.rollback()
            return 50102, dict_err.get(50102)

        try:
            sight.name = name
            sight.code = code
            sight.province_key = province
            sight.des = des
            sight.state = state
            sight.save()

            SightImg.objects.filter(sight=sight).delete()

            for img in imgs:
                SightImg.objects.create(sight=sight, img=img.replace('!600m0', ''))

            transaction.commit()
        except Exception, e:
            transaction.rollback()
            debug.get_debug_detail(e)
            return 99900, dict_err.get(99900)

        return 0, sight
