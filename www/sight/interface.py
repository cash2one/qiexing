# -*- coding: utf-8 -*-

from www.misc import consts
from www.sight.models import Sight, SightImg


dict_err = {
    50100: u'景点不存在或者已删除',
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
