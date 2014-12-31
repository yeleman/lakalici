#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import re
# import uuid
import random

from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        UserManager)
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from py3compat import implements_to_string

from manager.numbers import operator_from_malinumber, phonenumber_repr

logger = logging.getLogger(__name__)


def get_task_uuid():
    return Task.gen_uuid()


@implements_to_string
class Organization(models.Model):

    slug = models.SlugField()
    name = models.CharField(max_length=100)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def to_dict(self, with_balance=False):
        d = {
            'slug': self.slug,
            'name': self.name
        }
        if with_balance:
            d.update({'balance': self.balance})
        return d


@implements_to_string
class Contact(models.Model):
    ORANGE = 'orange'
    MALITEL = 'malitel'
    UNKNOWN = 'unknown'
    FOREIGN = 'foreign'

    OPERATORS = {
        ORANGE: "Orange Mali",
        MALITEL: "Malitel",
        FOREIGN: "Étranger",
        UNKNOWN: "Inconnu"
    }

    class Meta:
        unique_together = ['number', 'organization']

    name = models.CharField(
        verbose_name="Name",
        max_length=500, blank=True, null=True)
    number = models.CharField(
        verbose_name="Phone Number",
        max_length=100, unique=True)
    operator = models.CharField(
        verbose_name="Operator",
        max_length=50, choices=OPERATORS.items(), default=UNKNOWN)
    organization = models.ForeignKey(
        Organization, verbose_name="Organization",
        related_name='contacts')

    def __str__(self):
        return self.name if self.name else phonenumber_repr(self.number)

    def to_dict(self, with_organization=False):
        d = {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'number_str': phonenumber_repr(self.number),
            'operator': self.operator
        }
        if with_organization:
            d.update({'organization': self.organization.to_dict()})
        return d

    @classmethod
    def get_or_none(cls, cid):
        try:
            return cls.objects.get(id=cid)
        except cls.DoesNotExist:
            return None


@receiver(pre_save, sender=Contact)
def pre_save_update_contact_operator(sender, instance, **kwargs):
    instance.operator = operator_from_malinumber(instance.number)


@implements_to_string
class Group(models.Model):

    slug = models.SlugField()
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(Contact, related_name='groups')
    organization = models.ForeignKey(Organization, related_name='groups')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_none(cls, slug):
        try:
            return cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return None


@receiver(pre_save, sender=Group)
def iter_pre_save_handler(sender, instance, **kwargs):
    if not instance.pk:
        instance.slug = slugify(instance.name)


@implements_to_string
class Task(models.Model):

    CREATED = 'created'
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETE = 'complete'

    STATUSES = {
        CREATED: "Created",
        PENDING: "Pending",
        PROCESSING: "Processing",
        COMPLETE: "Complete"
    }

    AIRTIME = 'airtime'
    MPAYMENT = 'mpayment'
    ACTIONS = {
        AIRTIME: "Crédit mobile",
        MPAYMENT: "mPayment"
    }

    uid = models.CharField(max_length=50,
                           primary_key=True,
                           default=get_task_uuid)
    organization = models.ForeignKey(Organization, related_name='tasks')
    action = models.CharField(
        max_length=50, choices=ACTIONS.items(), default=AIRTIME)
    name = models.CharField(max_length=150)
    status = models.SlugField(choices=STATUSES.items(),
                              default=CREATED)

    def __str__(self):
        return self.name

    def to_dict(self, with_organization=False):
        d = {
            'id': self.uid,
            'name': self.name,
            'status': self.status,
            'action': self.action,
            'total_amount': self.total_amount(),
        }
        if with_organization:
            d.update({'organization': self.organization.to_dict()})
        return d

    @classmethod
    def gen_uuid(cls):
        # _gen = lambda: uuid.uuid4().hex[:6].upper()
        _gen = lambda: str(random.randint(100000, 999999)).zfill(6)
        uid = _gen()
        while cls.objects.filter(uid=uid).count():
            uid = _gen
        return uid

    @classmethod
    def get_or_none(cls, uid):
        try:
            return cls.objects.get(uid=uid)
        except cls.DoesNotExist:
            return None

    def total_amount(self):
        return sum([ti.amount for ti in self.task_items.all()])

    def contacts(self):
        return [ti.contact for ti in self.task_items.all()]


@receiver(pre_save, sender=Task)
def pre_save_set_name_if_none(sender, instance, **kwargs):
    if instance.name is None:
        instance.name = instance.uid


@implements_to_string
class TaskItem(models.Model):

    CREATED = 'created'
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETE = 'complete'

    STATUSES = {
        CREATED: "Created",
        PENDING: "Pending",
        PROCESSING: "Processing",
        COMPLETE: "Complete"
    }

    class Meta:
        unique_together = ['task', 'contact']

    task = models.ForeignKey(Task, related_name='task_items')
    contact = models.ForeignKey(Contact, related_name='task_items')
    amount = models.PositiveIntegerField(default=0)
    status = models.SlugField(choices=STATUSES.items(), default=CREATED)
    receipt = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "{amount} -> {contact}".format(
            amount=self.amount, contact=self.contact)

    @classmethod
    def get_or_none(cls, ti_id):
        try:
            return cls.objects.get(id=ti_id)
        except cls.DoesNotExist:
            return None

    def to_dict(self, with_task=True):
        d = {
            'id': self.id,
            'contact': self.contact.to_dict(),
            'amount': self.amount,
            'status': self.status
        }
        if with_task:
            d.update({'task': self.task.to_dict()})
        return d


@implements_to_string
class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(
        _("username"), max_length=50, primary_key=True,
        help_text=_("Required. 50 characters or fewer. "
                    "Letters, numbers and @/./+/-/_ characters"),
        validators=[validators.RegexValidator(re.compile("^[\w.@+-]+$"),
                    _("Enter a valid username."), "invalid")])

    first_name = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, blank=True, null=True,
                                 verbose_name=_("Last Name"))

    email = models.EmailField(_("email address"), blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"), default=False,
        help_text=_("Designates whether the user can "
                    "log into this admin site."))
    is_active = models.BooleanField(
        _("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    organization = models.ForeignKey(
        Organization, related_name='users', blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return self.name()

    def get_short_name(self):
        return self.name()

    def name(self):
        if not self.first_name and not self.last_name:
            return self.username
        elif not self.first_name:
            return self.last_name
        else:
            return self.first_name

    @classmethod
    def get_or_none(cls, username, with_inactive=False):
        qs = cls.objects if with_inactive else cls.active
        try:
            return qs.get(username=username)
        except cls.DoesNotExist:
            return None


class SMSMessage(models.Model):

    class Meta:
        verbose_name = _("SMS Message")
        verbose_name_plural = _("SMS Messages")

    INCOMING = 'incoming'
    OUTGOING = 'outgoing'
    DIRECTIONS = {
        INCOMING: _("Incoming"),
        OUTGOING: _("Outgoing")
    }

    SUCCESS = 'success'
    FAILURE = 'failure'
    BUFFERED = 'buffered'
    SMSC_SUBMIT = 'smsc_submit'
    SMSC_REJECT = 'smsc_reject'
    SMSC_NOTIFS = 'smsc_notifications'
    UNKNOWN = 'unknown'

    DELIVERY_STATUSES = {
        UNKNOWN: "Unknown",
        SUCCESS: "Delivery Success",
        FAILURE: "Delivery Failure",
        BUFFERED: "Message Buffered",
        SMSC_SUBMIT: "SMSC Submit",
        SMSC_REJECT: "SMSC Reject",
        SMSC_NOTIFS: "SMSC Intermediate Notifications",
    }

    direction = models.CharField(max_length=75,
                                 choices=DIRECTIONS.items())
    identity = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=timezone.now)
    event_on = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    handled = models.BooleanField(default=False)
    # minutes of validity
    validity = models.PositiveIntegerField(blank=True, null=True)
    # minutes after creation time to send the SMS at
    deferred = models.PositiveIntegerField(blank=True, null=True)
    # DLR statuses
    delivery_status = models.CharField(max_length=75, default=UNKNOWN,
                                       choices=DELIVERY_STATUSES.items())

    def str(self):
        return self.text

    @property
    def message(self):
        return self.text

    @property
    def content(self):
        return self.message

    def respond(self, text):
        SMSMessage.objects.create(
            direction=self.OUTGOING,
            identity=self.identity,
            event_on=timezone.now(),
            text=text)
