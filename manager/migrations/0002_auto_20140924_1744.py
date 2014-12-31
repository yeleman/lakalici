# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='balance',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='operator',
            field=models.CharField(choices=[('orange', 'Orange Mali'), ('malitel', 'Malitel'), ('unknown', 'Inconnu')], default='unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='organization',
            field=models.ForeignKey(related_name='tasks', to='manager.Organization'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.SlugField(choices=[('created', 'Created'), ('processing', 'Processing'), ('pending', 'Pending'), ('complete', 'Complete')], default='created'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='contact',
            field=models.ForeignKey(related_name='task_items', to='manager.Contact'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='status',
            field=models.SlugField(choices=[('created', 'Created'), ('processing', 'Processing'), ('pending', 'Pending'), ('complete', 'Complete')], default='created'),
        ),
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(blank=True, to='manager.Organization', null=True, related_name='users'),
        ),
    ]
