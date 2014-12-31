#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

logger = logging.getLogger(__name__)


def default_context(request, *args, **kwargs):
    context = {}

    if not request.user.is_authenticated \
            or not getattr(request.user, 'organization', None):
        return context

    context = {
        'account_balance': request.user.organization.balance,
        'groups': request.user.organization.groups,
        'contacts': request.user.organization.contacts,
        'tasks': request.user.organization.tasks,
    }
    return context
