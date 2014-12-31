# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20140924_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(verbose_name='Name', max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='number',
            field=models.CharField(verbose_name='Phone Number', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='operator',
            field=models.CharField(verbose_name='Operator', max_length=50, choices=[('orange', 'Orange Mali'), ('unknown', 'Inconnu'), ('foreign', 'Étranger'), ('malitel', 'Malitel')], default='unknown'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(related_name='contacts', verbose_name='Organization', to='manager.Organization'),
        ),
        migrations.AlterUniqueTogether(
            name='taskitem',
            unique_together=set([('task', 'contact')]),
        ),
    ]
