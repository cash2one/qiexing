# -*- coding: utf-8 -*-

import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'


user_id = user = 'b2d540e11c7511e48083685b35d0bf16'


def main():
    import datetime
    from www.activity import interface
    from www.account.models import User

    ab = interface.ActivityBase()
    apb = interface.ActivityPersonBase()

    activity = ab.get_activity_by_id(1)
    request_user = User.objects.get(id=user_id)
    # user_id_1 = u"48f23e751c7c11e494eb685b35d0bf16"
    # print apb.join_activity(activity, user_id, real_name=u"简单的快乐", mobile=u"13005012270", partner_count=5, state=True)
    print apb.set_join_state(activity, request_user, 2, True)


if __name__ == '__main__':
    main()
