# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.admin.views',
                       url(r'^$', 'home'),
                       )


# 提问
urlpatterns += patterns('www.admin.views_sight',

                        url(r'^sight/get_province_by_name$', 'get_province_by_name'),
                        url(r'^sight/get_sight_by_id$', 'get_sight_by_id'),
                        url(r'^sight/modify_sight$', 'modify_sight'),
                        url(r'^sight/remove_sight$', 'remove_sight'),
                        url(r'^sight/add_sight$', 'add_sight'),
                        url(r'^sight/search$', 'search'),
                        url(r'^sight$', 'sight'),
                        )


# 用户
urlpatterns += patterns('www.admin.views_user',

                        url(r'^user/modify_user$', 'modify_user'),
                        url(r'^user/get_user_by_id$', 'get_user_by_id'),
                        url(r'^user/search$', 'search'),
                        url(r'^user$', 'user'),
                        )

# 友情链接
urlpatterns += patterns('www.admin.views_friendly_link',

                        url(r'^friendly_link/modify_friendly_link$', 'modify_friendly_link'),
                        url(r'^friendly_link/remove_friendly_link$', 'remove_friendly_link'),
                        url(r'^friendly_link/get_friendly_link_by_id$', 'get_friendly_link_by_id'),
                        url(r'^friendly_link/add_friendly_link$', 'add_friendly_link'),
                        url(r'^friendly_link/search$', 'search'),
                        url(r'^friendly_link$', 'friendly_link'),
                        )

# 权限
urlpatterns += patterns('www.admin.views_permission',

                        url(r'^permission/cancel_admin$', 'cancel_admin'),
                        url(r'^permission/save_user_permission$', 'save_user_permission'),
                        url(r'^permission/get_user_permissions$', 'get_user_permissions'),
                        url(r'^permission/get_all_administrators$', 'get_all_administrators'),
                        url(r'^permission$', 'permission'),
                        )

# 用户
urlpatterns += patterns('www.admin.views_sign',

                        url(r'^sign/sign_in_pass$', 'sign_in_pass'),
                        url(r'^sign/sign_in_fail$', 'sign_in_fail'),
                        url(r'^sign/search$', 'search'),
                        url(r'^sign$', 'sign'),
                        )


# 用户
urlpatterns += patterns('www.admin.views_cover',

                        url(r'^home_cover/add_cover$', 'add_cover'),
                        url(r'^home_cover/remove_cover$', 'remove_cover'),
                        url(r'^home_cover/modify_cover$', 'modify_cover'),
                        url(r'^home_cover/get_cover_by_id$', 'get_cover_by_id'),
                        url(r'^home_cover/search$', 'search'),
                        url(r'^home_cover$', 'home_cover'),
                        )
