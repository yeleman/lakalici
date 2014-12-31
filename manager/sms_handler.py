#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import re

from django.utils import timezone

from manager.models import Task, TaskItem
from manager.numbers import normalized_phonenumber

logger = logging.getLogger(__name__)


def test(message, **kwargs):
    msg = "Received on {date}"
    try:
        _, content = message.content.split()
        msg += ": {content}"
    except:
        pass

    message.respond(msg.format(date=timezone.now(), content=content))
    return True


def echo(message, **kwargs):
    message.respond(kwargs['args'])
    return True


def orange_airtime_status_update(message, **kwargs):
    reg = r'210:Vous avez recharge avec success le ([0-9]{8}) ' \
          r'Montant : ([0-9]+) FCFA N TXN :([A-Z0-9\.]+) . ' \
          r'Nouveau solde : ([0-9]+) FCFA.'
    try:
        number, amount, txn, balance = \
            re.match(reg, message.content.strip()).groups()
        clean_number = normalized_phonenumber(number)
        amount = int(amount)
        balance = int(balance)
    except:
        logger.error(
            "Failed to decode airtime status update for m#{id}: {txt}"
            .format(id=message.id, txt=message.content))
        return False

    # find matching TaskItem
    qs = TaskItem.objects.filter(
        status__in=(TaskItem.PENDING, TaskItem.PROCESSING),
        contact__number=clean_number,
        amount=amount,
        task__status__in=(Task.PENDING, Task.PROCESSING, Task.COMPLETE))
    if qs.count() == 0:
        logger.error("Unable to match receipt for m#{}".format(message.id))
    elif qs.count() > 1:
        logger.error(
            "CONFLICT m#{}. {} matching TaskItems"
            .format(message.id, qs.count()))
    else:
        ti = qs.get()
        ti.status = ti.COMPLETE
        ti.receipt = txn
        ti.save()

        logger.info(
            "Updated TI#{} with receipt {}."
            .format(ti.id, ti.receipt))

        logger.info(
            "New Orange Airtime Balance (from receipt): {}".format(balance))
    return True


def orange_airtime_balance_update(message, **kwargs):
    logger.info("")
    try:
        balance = message.content.rsplit(':', 1)[1]
    except IndexError:
        balance = None
    if balance is not None:
        logger.info("New Orange Aitime Balance: {}".format(balance))
        pass
    return True


def orange_airtime(message, **kwargs):
    logger.debug("Received feedback message for Orange mugan-mugan")

    if message.content.startswith('210:'):
        return orange_airtime_status_update(message, **kwargs)
    if message.content.startswith('4300:'):
        return orange_airtime_balance_update(message, **kwargs)
    return True


def malitel_airtime(message, **kwargs):
    logger.error("Not Implemented Airtime to Malitel Feedback")
    return True


def orange_mpayment(message, **kwargs):
    logger.error("Not Implemented mPayment to Orange Feedback")
    return True


def malitel_mpayment(message, **kwargs):
    logger.error("Not Implemented mPayment to Malitel Feedback")
    return True


def all_incoming(message, **kwargs):

    is_airtime_feedback = False
    is_mpayment_feedback = False
    is_orange = False
    is_malitel = False

    # filter action based on identity
    if message.identity == '+37579':
        is_orange = True
        is_airtime_feedback = True

    if is_airtime_feedback and is_orange:
        return orange_airtime(message, **kwargs)

    if is_airtime_feedback and is_malitel:
        return malitel_airtime(message, **kwargs)

    if is_mpayment_feedback and is_orange:
        return orange_mpayment(message, **kwargs)

    if is_mpayment_feedback and is_malitel:
        return malitel_mpayment(message, **kwargs)

    logger.debug("Incoming message was not handled: {}"
                 .format(message.content))
    return False


def lklc_sms_handler(message):

    logger.debug("Incoming SMS from {}: {}".format(
        message.identity, message.content))

    keywords = {'test': test,
                'echo': echo}

    for keyword, handler in keywords.items():
        if message.content.lower().startswith(keyword):
            return handler(message)

    return all_incoming(message)

    # message.respond("Message non pris en charge.")
    return False
