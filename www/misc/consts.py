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
    u"海南": [7, u"hainan"],
    u"云南": [8, u"yunnan"],
    u"福建": [9, u"fujian"],
    u"江西": [10, u"jiangxi"],
    u"湖南": [11, u"hunan"],
    u"贵州": [12, u"guizhou"],
    u"浙江": [13, u"zhejiang"],
    u"安徽": [14, u"anhui"],
    u"上海": [15, u"shanghai"],
    u"江苏": [16, u"jiangsu"],
    u"湖北": [17, u"hubei"],
    u"西藏": [18, u"xizang"],
    u"青海": [19, u"qinghai"],
    u"甘肃": [20, u"gansu"],
    u"新疆": [21, u"xinjiang"],
    u"陕西": [22, u"shanxis"],
    u"河南": [23, u"henan"],
    u"山西": [24, u"shanxi"],
    u"山东": [25, u"shandong"],
    u"河北": [26, u"hebei"],
    u"天津": [27, u"tianjin"],
    u"北京": [28, u"beijing"],
    u"宁夏": [29, u"ningxia"],
    u"内蒙古": [30, u"neimeng"],
    u"辽宁": [31, u"liaoning"],
    u"吉林": [32, u"jilin"],
    u"黑龙江": [33, u"heilongjiang"],
    u"重庆": [34, u"chongqing"]
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

    {'code': 'cover_manage', 'name': u'首页封面管理', 'parent': None},
    {'code': 'save_home_cover', 'name': u'修改首页封面', 'parent': 'cover_manage'},
    {'code': 'query_home_cover', 'name': u'查询首页封面', 'parent': 'cover_manage'},
    {'code': 'remove_home_cover', 'name': u'删除首页封面', 'parent': 'cover_manage'},
    {'code': 'add_home_cover', 'name': u'添加首页封面', 'parent': 'cover_manage'},

    {'code': 'static_manage', 'name': u'静态页面管理', 'parent': None},
    {'code': 'save_static_page', 'name': u'修改静态页面', 'parent': 'static_manage'},
]
