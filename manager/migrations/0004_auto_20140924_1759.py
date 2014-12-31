# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20140924_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='organization',
            field=models.ForeignKey(related_name='groups', to='manager.Organization', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='operator',
            field=models.CharField(default='unknown', choices=[('orange', 'Orange Mali'), ('malitel', 'Malitel'), ('unknown', 'Inconnu')], max_length=50),
        ),
        migrations.AlterField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(related_name='contacts', to='manager.Organization'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.SlugField(default='created', choices=[('processing', 'Processing'), ('created', 'Created'), ('complete', 'Complete'), ('pending', 'Pending')]),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='status',
            field=models.SlugField(default='created', choices=[('processing', 'Processing'), ('created', 'Created'), ('complete', 'Complete'), ('pending', 'Pending')]),
        ),
    ]
