# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20140925_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='action',
            field=models.CharField(choices=[('airtime', 'Crédit mobile'), ('mpayment', 'mPayment')], default='airtime', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='operator',
            field=models.CharField(verbose_name='Operator', default='unknown', choices=[('foreign', 'Étranger'), ('unknown', 'Inconnu'), ('malitel', 'Malitel'), ('orange', 'Orange Mali')], max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.SlugField(choices=[('complete', 'Complete'), ('created', 'Created'), ('processing', 'Processing'), ('pending', 'Pending')], default='created'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='status',
            field=models.SlugField(choices=[('complete', 'Complete'), ('created', 'Created'), ('processing', 'Processing'), ('pending', 'Pending')], default='created'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='task',
            field=models.ForeignKey(to='manager.Task', related_name='task_items'),
        ),
    ]
