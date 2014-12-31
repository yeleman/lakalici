# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_auto_20140926_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('direction', models.CharField(max_length=75, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')])),
                ('identity', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('event_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
                ('handled', models.BooleanField(default=False)),
                ('validity', models.PositiveIntegerField(blank=True, null=True)),
                ('deferred', models.PositiveIntegerField(blank=True, null=True)),
                ('delivery_status', models.CharField(max_length=75, default='unknown', choices=[('unknown', 'Unknown'), ('smsc_reject', 'SMSC Reject'), ('buffered', 'Message Buffered'), ('failure', 'Delivery Failure'), ('smsc_submit', 'SMSC Submit'), ('smsc_notifications', 'SMSC Intermediate Notifications'), ('success', 'Delivery Success')])),
            ],
            options={
                'verbose_name': 'SMS Message',
                'verbose_name_plural': 'SMS Messages',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='taskitem',
            name='receipt',
            field=models.CharField(blank=True, max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='operator',
            field=models.CharField(verbose_name='Operator', max_length=50, default='unknown', choices=[('foreign', 'Étranger'), ('unknown', 'Inconnu'), ('orange', 'Orange Mali'), ('malitel', 'Malitel')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='action',
            field=models.CharField(max_length=50, default='airtime', choices=[('airtime', 'Crédit mobile'), ('mpayment', 'mPayment')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.SlugField(default='created', choices=[('pending', 'Pending'), ('processing', 'Processing'), ('complete', 'Complete'), ('created', 'Created')]),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='status',
            field=models.SlugField(default='created', choices=[('pending', 'Pending'), ('processing', 'Processing'), ('complete', 'Complete'), ('created', 'Created')]),
        ),
    ]
