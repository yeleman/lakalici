# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20140924_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=150)),
                ('members', models.ManyToManyField(to='manager.Contact', related_name='groups')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='contact',
            name='operator',
            field=models.CharField(choices=[('unknown', 'Inconnu'), ('malitel', 'Malitel'), ('orange', 'Orange Mali')], default='unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.SlugField(choices=[('pending', 'Pending'), ('complete', 'Complete'), ('processing', 'Processing'), ('created', 'Created')], default='created'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='status',
            field=models.SlugField(choices=[('pending', 'Pending'), ('complete', 'Complete'), ('processing', 'Processing'), ('created', 'Created')], default='created'),
        ),
    ]
