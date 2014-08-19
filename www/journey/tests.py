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
    from www.journey import interface

    jb = interface.JourneyBase()
    print jb.cancel_top(1)


if __name__ == '__main__':
    main()
