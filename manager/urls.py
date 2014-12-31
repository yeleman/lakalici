#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',

    # Android API
    url(r'^fondasms/?$', 'fondasms.views.fondasms_handler',
        {'handler_module': 'manager.fondasms_handlers',
         'send_automatic_reply': False,
         'automatic_reply_via_handler': False,
         'automatic_reply_text': None},
        name='fondasms'),
    url(r'^fondasms/test/?$',
        TemplateView.as_view(template_name="fondasms_tester.html"),
        name='fondasms_tester'),

    url(r'^/?$', 'manager.views.about', name='about'),
    url(r'^groups/?$', 'manager.views.groups', name='groups'),
    url(r'^groups/(?P<slug>[a-zA-Z0-9\-]+)/?$',
        'manager.views.group_detail', name='group'),
    url(r'^groups/(?P<slug>[a-zA-Z0-9\-]+)/remove/(?P<contact_id>[0-9]+)/?$',
        'manager.views.group_contact_remove', name='group_contact_remove'),
    url(r'^groups/(?P<slug>[a-zA-Z0-9\-]+)/remove/?$',
        'manager.views.group_remove', name='group_delete'),
    url(r'^account/?$', 'manager.views.account', name='account'),
    url(r'^contacts/?$', 'manager.views.contacts', name='contacts'),
    url(r'^contacts/import/?$', 'manager.views.import_contacts',
        name='import_contacts'),
    url(r'^tasks/?$', 'manager.views.tasks', name='tasks'),
    url(r'^tasks/new/?$', 'manager.views.new_task', name='new_task'),
    url(r'^tasks/(?P<uid>[a-zA-Z0-9]+)/?$',
        'manager.views.task_detail', name='task'),

    url(r'^api/tasks/(?P<uid>[a-zA-Z0-9]+)/?$',
        'manager.views.api_task', name='api_task'),
    url(r'^api/tasks/(?P<uid>[a-zA-Z0-9]+)/update/?$',
        'manager.views.api_task_update', name='api_task_update'),
    url(r'^api/items/(?P<item_id>[a-zA-Z0-9]+)/update?$',
        'manager.views.api_item_update', name='api_item_update'),
)
