#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django import forms
# import floppyforms.__future__ as forms

# from manager.models import Contact
from manager.numbers import normalized_phonenumber

logger = logging.getLogger(__name__)


class AddGroupForm(forms.Form):

    name = forms.CharField(
        label="Nom du groupe",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "Nom du groupe"}))


class AddSingleContact(forms.Form):

    number = forms.CharField(
        max_length=75,
        required=True,
        label="Number",
        help_text="If not a Mali number, use +indicator syntax.")

    name = forms.CharField(max_length=500, required=False)

    def clean_number(self):
        numbersent = self.cleaned_data.get('number')
        normalized = normalized_phonenumber(numbersent)
        if normalized is None:
            raise forms.ValidationError("Invalid Phone Number: %(value)s",
                                        code='invalid',
                                        params={'value': numbersent})
        return normalized


class ImportContactsFile(forms.Form):

    ACTIONS = {
        'create_group': "Créer un nouveau groupe",
        'add_to_group': "Ajouter au groupe",
        'reset_group': "Remplacer le groupe"
    }

    xls_file = forms.FileField(required=True, label="Fichier Excel")
    action = forms.ChoiceField(required=True, label="Destination")
    group = forms.ChoiceField(required=False, label="Groupe")
    group_name = forms.CharField(required=False, label="Nouveau groupe")

    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization')
        super(ImportContactsFile, self).__init__(*args, **kwargs)

        self.fields['action'].choices = self.ACTIONS.items()
        self.fields['group'].choices = [
            (g.slug, g.name) for g in organization.groups.all()]
