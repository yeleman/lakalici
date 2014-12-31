#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import tempfile
import unicodedata

from django.utils import timezone

from manager.models import Contact, Group, Task, TaskItem, SMSMessage
from manager.numbers import normalized_phonenumber

logger = logging.getLogger(__name__)


def send_sms(to, text):

    return SMSMessage.objects.create(
        direction=SMSMessage.OUTGOING,
        identity=to,
        event_on=timezone.now(),
        text=text)


def to_ascii(text):
    return unicodedata.normalize('NFKD', unicode(text)) \
                      .encode('ASCII', 'ignore').strip()


def store_uploaded_file(f):
    tmpf = tempfile.NamedTemporaryFile(mode='wb+', suffix='.xls', delete=False)
    for chunk in f.chunks():
        tmpf.write(chunk)
    tmpf.close()
    return tmpf.name


def import_path(name, failsafe=False):
    """ import a callable from full module.callable name """
    def _imp(name):
        modname, __, attr = name.rpartition('.')
        if not modname:
            # single module name
            return __import__(attr)
        m = __import__(modname, fromlist=[str(attr)])
        return getattr(m, attr)
    try:
        return _imp(name)
    except (ImportError, AttributeError) as exp:
        logger.debug("Failed to import {}: {}".format(name, exp))
        if failsafe:
            return None
        raise exp


def create_contact(number, organization, name=None):
    created = updated = False

    number = normalized_phonenumber(number)

    qs = Contact.objects.filter(number=number, organization=organization)
    if qs.count():
        contact = qs.get()
        if name and contact.name != name:
            contact.name = name
            contact.save()
            updated = True
    else:
        contact = Contact.objects.create(
            number=number,
            name=name,
            organization=organization)
        created = True

    return created, updated, contact


def add_contact_to_group(contact, group):
    added = False
    if contact not in group.members.all():
        group.members.add(contact)
        added = True
    return added


def remove_contact_from_group(contact, group):
    removed = False
    if contact in group.members.all():
        group.members.remove(contact)
        removed = True
    return removed


def create_group(name, organization):
    created = False
    qs = Group.objects.filter(name=name, organization=organization)
    if not qs.count():
        group = Group.objects.create(
            name=name,
            organization=organization)
        created = True
    else:
        group = qs.get()
    return created, group


def delete_group(group):
    deleted = False
    if group:
        group.delete()
        deleted = True
    return deleted


def create_task(name, organization):
    created = False
    task = Task.objects.create(name=name, organization=organization)
    created = True
    return created, task


def add_contact_to_task(contact, task, amount=0):
    added = False
    qs = TaskItem.objects.filter(contact=contact, task=task)
    if qs.count():
        return qs.get()
    else:
        task_item = TaskItem.objects.create(
            contact=contact, task=task, amount=amount)
        added = True
    return added, task_item
