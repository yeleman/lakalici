#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.contrib import admin

from manager.models import Contact, Organization, Task, TaskItem, User

logger = logging.getLogger(__name__)

admin.site.register(Contact)
admin.site.register(Organization)
admin.site.register(Task)
admin.site.register(TaskItem)
admin.site.register(User)
