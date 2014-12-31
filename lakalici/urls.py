#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.conf.urls import patterns, include, url
from django.contrib import admin
from manager import urls as manager_urls

logger = logging.getLogger(__name__)

urlpatterns = patterns(
    '',
    url(r'', include(manager_urls)),

    # authentication
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)
