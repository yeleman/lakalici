# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
import re
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', help_text='Required. 50 characters or fewer. Letters, numbers and @/./+/-/_ characters', max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Enter a valid username.', 'invalid')], primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, null=True, verbose_name='First Name', max_length=100)),
                ('last_name', models.CharField(blank=True, null=True, verbose_name='Last Name', max_length=100)),
                ('email', models.EmailField(blank=True, null=True, verbose_name='email address', max_length=75)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, null=True, max_length=500)),
                ('number', models.CharField(max_length=100, unique=True)),
                ('operator', models.CharField(max_length=50, choices=[('malitel', 'Malitel'), ('unknown', 'Inconnu'), ('orange', 'Orange Mali')], default='unknown')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('uid', models.CharField(primary_key=True, default=manager.models.get_task_uuid, serialize=False, max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('status', models.SlugField(default='created', choices=[('pending', 'Pending'), ('complete', 'Complete'), ('created', 'Created'), ('processing', 'Processing')])),
                ('organization', models.ForeignKey(to='manager.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('status', models.SlugField(default='created', choices=[('pending', 'Pending'), ('complete', 'Complete'), ('created', 'Created'), ('processing', 'Processing')])),
                ('contact', models.ForeignKey(to='manager.Contact')),
                ('task', models.ForeignKey(to='manager.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(to='manager.Organization'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('number', 'organization')]),
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(null=True, blank=True, to='manager.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', related_query_name='user', help_text='Specific permissions for this user.', blank=True, related_name='user_set'),
            preserve_default=True,
        ),
    ]
