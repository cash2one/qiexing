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
