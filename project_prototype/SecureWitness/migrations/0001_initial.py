# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('file', models.FileField(default='', upload_to='SecureWitness/', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('name', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('file', models.OneToOneField(to='SecureWitness.File', serialize=False, primary_key=True)),
                ('key', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('title', models.CharField(default='', max_length=300, serialize=False, primary_key=True)),
                ('authorName', models.CharField(default='', max_length=30, blank=True)),
                ('user_perm', models.TextField(default='', blank=True)),
                ('group_perm', models.TextField(default='', blank=True)),
                ('access_type', models.BooleanField(default=False)),
                ('timestamp', models.TextField(default='', blank=True)),
                ('shortDesc', models.TextField(default='', blank=True)),
                ('detailsDesc', models.TextField(default='', blank=True)),
                ('dateOfIncident', models.TextField(default='', blank=True, null=True)),
                ('locationOfIncident', models.TextField(default='', blank=True, null=True)),
                ('keywords', models.TextField(default='', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('requester', models.CharField(default='', max_length=100)),
                ('group', models.ForeignKey(to='SecureWitness.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('admin_status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='authorId',
            field=models.ForeignKey(to='SecureWitness.UserProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='report',
            field=models.ForeignKey(to='SecureWitness.Report'),
            preserve_default=True,
        ),
    ]
