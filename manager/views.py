#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.http import Http404, JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from manager.models import Group, Contact, Task, TaskItem
from manager.forms import AddGroupForm, AddSingleContact, ImportContactsFile
from manager.numbers import phonenumber_repr
from manager.utils import (
    create_contact, add_contact_to_group, create_group,
    remove_contact_from_group, delete_group,
    store_uploaded_file, create_task, add_contact_to_task)
from manager.xls_import import handle_xls_file

logger = logging.getLogger(__name__)


def about(request, **kwargs):
    context = {'domain': 'about'}
    return render(request, kwargs.get('template_name', 'about.html'), context)


@login_required
def account(request, **kwargs):
    context = {'domain': 'account'}
    return render(request,
                  kwargs.get('template_name', 'account.html'),
                  context)


@login_required
def tasks(request, **kwargs):
    context = {'domain': 'tasks'}
    return render(request,
                  kwargs.get('template_name', 'tasks.html'),
                  context)


@login_required
def groups(request, **kwargs):
    context = {'domain': 'groups'}

    if request.method == "POST":
        form = AddGroupForm(request.POST)
        if form.is_valid():
            created, group = create_group(
                name=form.cleaned_data.get('name').strip(),
                organization=request.user.organization)
            if created:
                messages.info(
                    request, "Le groupe {} a été créé.".format(group))
            else:
                messages.warning(
                    request, "Le groupe {} existe déjà.".format(group))
            redirect('groups')
    else:
        form = AddGroupForm()

    context.update({'form': form})
    return render(request,
                  kwargs.get('template_name', 'groups.html'),
                  context)


@login_required
def group_detail(request, slug, **kwargs):
    context = {'domain': 'groups'}
    group = Group.get_or_none(slug)
    if groups is None:
        raise Http404("No Group with slug `{}`".format(slug))
    context.update({'group': group})
    if request.method == "POST":
        form = AddSingleContact(request.POST)
        if form.is_valid():
            created, updated, contact = create_contact(
                number=form.cleaned_data.get('number'),
                organization=request.user.organization,
                name=form.cleaned_data.get('name').strip())
            if created:
                messages.info(
                    request, "Le contact {} a été créé.".format(contact))
            if updated:
                messages.info(
                    request,
                    "Le nom du contact {} a été changé pour {}"
                    .format(phonenumber_repr(contact.number), contact.name))

            added_to_group = add_contact_to_group(contact, group)
            if added_to_group:
                messages.info(request,
                              "Le contact {} a été ajouté au groupe {}."
                              .format(contact, group))
            redirect('group', slug=group.slug)
    else:
        form = AddSingleContact()

    context.update({'form': form})

    return render(request,
                  kwargs.get('template_name', 'group.html'),
                  context)


@login_required
def group_contact_remove(request, slug, contact_id, **kwargs):
    group = Group.get_or_none(slug)
    if groups is None:
        raise Http404("No Group with slug `{}`".format(slug))
    contact = Contact.get_or_none(contact_id)
    if contact is None:
        raise Http404("No Contact with id `{}`".format(contact_id))
    removed = remove_contact_from_group(contact, group)
    if removed in group.members.all():
        messages.info(
            request,
            "Le contact {} a été enlevé du groupe {}"
            .format(contact, group))
    else:
        messages.warning(
            request,
            "Le contact {} ne fait pas partie du groupe {}."
            .format(contact, group))
    return redirect('group', slug=slug)


@login_required
def group_remove(request, slug, **kwargs):
    group = Group.get_or_none(slug)
    if groups is None:
        raise Http404("No Group with slug `{}`".format(slug))
    deleted = delete_group(group)
    if deleted:
        messages.info(request, "Le groupe {} a été supprimé.".format(group))
    else:
        messages.warning(request, "Le groupe {} a n'existe pas.".format(group))
    return redirect('groups')


@login_required
def contacts(request, **kwargs):
    context = {'domain': 'contacts'}
    return render(request,
                  kwargs.get('template_name', 'contacts.html'),
                  context)


@login_required
def import_contacts(request, **kwargs):
    context = {'domain': 'contacts'}

    if request.method == "POST":
        form = ImportContactsFile(request.POST,
                                  request.FILES,
                                  organization=request.user.organization)
        if form.is_valid():
            fpath = store_uploaded_file(request.FILES['xls_file'])
            action = form.cleaned_data.get('action')
            group_name = form.cleaned_data.get('group_name')
            group = form.cleaned_data.get('group')
            if action == 'create_group':
                created, group = create_group(
                    name=group_name, organization=request.user.organization)
                if created:
                    messages.info(
                        request, "Le groupe {} a été créé.".format(group))

            numbers = {
                'nb_created': 0,
                'nb_updated': 0,
                'nb_added_to_group': 0
            }
            # nb_created = nb_updated = nb_added_to_group = 0

            def handle_row(number, name, organization, numbers):
                # global nb_created, nb_updated, nb_added_to_group
                created, updated, contact = create_contact(
                    number=number,
                    organization=request.user.organization,
                    name=name)
                numbers['nb_created'] += 1 if created else 0
                numbers['nb_updated'] += 1 if updated else 0
                added = add_contact_to_group(contact, group)
                numbers['nb_added_to_group'] += 1 if added else 0

            handle_xls_file(
                fpath=fpath,
                handle_row=handle_row,
                organization=request.user.organization,
                numbers=numbers)

            messages.info(
                request,
                "{nbc} contacts ont été créés. {nbu} ont été modifiés et "
                "{nba} ont été ajouté au groupe {group}"
                .format(nbc=numbers['nb_created'], nbu=numbers['nb_updated'],
                        nba=numbers['nb_added_to_group'], group=group))

            redirect('group', group.slug)
    else:
        form = ImportContactsFile(
            initial={'action': 'create_group',
                     'group_name': timezone.now().strftime('%d-%m-%Y')},
            organization=request.user.organization)

    context.update({'form': form})
    return render(request,
                  kwargs.get('template_name', 'import_contacts.html'),
                  context)


@login_required
def new_task(request, **kwargs):
    contact_ids = request.POST.getlist('contact_ids')
    name = request.POST.get('name')
    if not len(contact_ids):
        messages.error(
            request,
            "Impossible de créer une tâche sans contacts.")
        return redirect('tasks')

    created, task = create_task(name=name,
                                organization=request.user.organization)
    if created:
        messages.info(
            request,
            "La tâche {} a été créée.".format(task))
    else:
        messages.warning(
            request,
            "La tâche {} n'a pas été créée".format(task))
    nb_added = 0
    for cid in contact_ids:
        contact = Contact.get_or_none(cid)
        added, ti = add_contact_to_task(contact, task, amount=0)
        if added:
            nb_added += 1
    messages.info(
        request,
        "{} contacts ont été ajoutés à la tâche {}".format(nb_added, task))

    return redirect('tasks')


@login_required
def task_detail(request, uid, **kwargs):
    context = {'domain': 'tasks'}
    task = Task.get_or_none(uid)
    if task is None:
        raise Http404("No Task with id `{}`".format(uid))
    context.update({'task': task})

    return render(request,
                  kwargs.get('template_name', 'task.html'),
                  context)


def api_task(request, uid):
    task = Task.get_or_none(uid)
    data = task.to_dict()
    data.update({'items': [ti.to_dict(with_task=False)
                           for ti in task.task_items.all()]})
    return JsonResponse(data, safe=False)


@require_POST
@csrf_exempt
def api_task_update(request, uid):
    task = Task.get_or_none(uid)
    updated = False
    new_status = request.POST.get('status')
    if new_status in Task.STATUSES.keys():
        task.status = new_status
        task.save()
        updated = True
    data = {"updated": updated}
    return JsonResponse(data, safe=False)


@require_POST
@csrf_exempt
def api_item_update(request, item_id):
    ti = TaskItem.get_or_none(item_id)
    updated = False
    new_status = request.POST.get('status')
    if new_status in TaskItem.STATUSES.keys():
        ti.status = new_status
        ti.save()
        updated = True
    data = {"updated": updated}
    return JsonResponse(data, safe=False)
