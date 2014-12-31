#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import locale

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

from manager.numbers import phonenumber_repr
from manager.utils import import_path

register = template.Library()
locale.setlocale(locale.LC_ALL, '')


@register.filter(name='phone')
@stringfilter
def phone_number_formatter(number):
    ''' format phone number properly for display '''
    return phonenumber_repr(number)


@register.filter(name='carrier')
@stringfilter
def carrier_repr_from_slug(slug):
    try:
        # in case slug is an actual Contact
        slug = slug.operator
    except:
        pass

    return settings.OPERATORS.get(slug, [None])[0]


@register.filter(name='verbose')
@stringfilter
def verbose_from_dict(value, dictpath):
    m, d = dictpath.rsplit('.', 1)
    m = import_path("manager.models.{}".format(m), failsafe=True)
    data = getattr(m, d, {})
    return data.get(value, None)
