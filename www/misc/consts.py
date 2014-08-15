# -*- coding: utf-8 -*-

'''
全局常量维护
'''

G_DICT_ERROR = {
    99600: u'不存在的用户',
    99700: u'权限不足',
    99800: u'参数缺失',
    99900: u'系统错误',
    0: u'成功'
}

G_PROVINCE = {
    u"澳门": [1, u"aomen"],
    u"香港": [2, u"hk"],
    u"台湾": [3, u"taiwan"],
    u"广东": [4, u"guangdong"],
    u"广西": [5, u"guangxi"],
    u"四川": [6, u"sichuan"],
}


PERMISSIONS = [
    {'code': 'permission_manage', 'name': u'权限管理', 'parent': None},
    {'code': 'add_user_permission', 'name': u'添加用户权限', 'parent': 'permission_manage'},
    {'code': 'query_user_permission', 'name': u'查询用户权限', 'parent': 'permission_manage'},
    {'code': 'modify_user_permission', 'name': u'修改用户权限', 'parent': 'permission_manage'},
    {'code': 'cancel_admin', 'name': u'取消管理员', 'parent': 'permission_manage'},

    {'code': 'user_manage', 'name': u'用户管理', 'parent': None},
    #{'code': 'add_user', 'name': u'添加用户', 'parent': 'user_manage'},
    {'code': 'query_user', 'name': u'查询用户', 'parent': 'user_manage'},
    {'code': 'modify_user', 'name': u'修改用户', 'parent': 'user_manage'},
    {'code': 'remove_user', 'name': u'删除用户', 'parent': 'user_manage'},

    {'code': 'friendly_link_manage', 'name': u'友情链接管理', 'parent': None},
    {'code': 'add_friendly_link', 'name': u'添加友情链接', 'parent': 'friendly_link_manage'},
    {'code': 'query_friendly_link', 'name': u'查询友情链接', 'parent': 'friendly_link_manage'},
    {'code': 'modify_friendly_link', 'name': u'修改友情链接', 'parent': 'friendly_link_manage'},
    {'code': 'remove_friendly_link', 'name': u'删除友情链接', 'parent': 'friendly_link_manage'},

    {'code': 'sight_manage', 'name': u'景点管理', 'parent': None},
    {'code': 'add_sight', 'name': u'添加景点', 'parent': 'sight_manage'},
    {'code': 'query_sight', 'name': u'查询景点', 'parent': 'sight_manage'},
    {'code': 'modify_sight', 'name': u'修改景点', 'parent': 'sight_manage'},
    {'code': 'remove_sight', 'name': u'删除景点', 'parent': 'sight_manage'},

    {'code': 'sign_manage', 'name': u'报名管理', 'parent': None},
    {'code': 'sign_in_pass', 'name': u'报名通过', 'parent': 'sign_manage'},
    {'code': 'sign_in_fail', 'name': u'报名失败', 'parent': 'sign_manage'},
    {'code': 'query_sign', 'name': u'查询报名列表', 'parent': 'sign_manage'},

    # {'code': 'friendly_link_manage', 'name': u'报名管理', 'parent': None},
    # {'code': 'add_friendly_link', 'name': u'添加友情链接', 'parent': 'friendly_link_manage'},
    # {'code': 'query_friendly_link', 'name': u'查询友情链接', 'parent': 'friendly_link_manage'},
    # {'code': 'modify_friendly_link', 'name': u'修改友情链接', 'parent': 'friendly_link_manage'},
    # {'code': 'remove_friendly_link', 'name': u'删除友情链接', 'parent': 'friendly_link_manage'},
]
