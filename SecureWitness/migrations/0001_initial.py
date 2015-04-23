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
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('comment', models.TextField(default='', blank=True)),
                ('authorName', models.CharField(max_length=30, default='', blank=True)),
                ('timestamp', models.TextField(default='', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to='SecureWitness/', blank=True, default='', null=True)),
                ('fileType', models.CharField(max_length=200, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('file', models.OneToOneField(to='SecureWitness.File', primary_key=True, serialize=False)),
                ('key', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=300, default='')),
                ('authorName', models.CharField(max_length=30, default='', blank=True)),
                ('folder', models.IntegerField(default='0', blank=True)),
                ('user_perm', models.TextField(default='', blank=True)),
                ('access_type', models.BooleanField(default=False)),
                ('timestamp', models.TextField(default='', blank=True)),
                ('shortDesc', models.TextField(default='', blank=True)),
                ('detailsDesc', models.TextField(default='', blank=True)),
                ('dateOfIncident', models.TextField(blank=True, default='', null=True)),
                ('locationOfIncident', models.TextField(blank=True, default='', null=True)),
                ('keywords', models.TextField(blank=True, default='', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('requester', models.CharField(max_length=100, default='')),
                ('group', models.ForeignKey(to='SecureWitness.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
            model_name='report',
            name='group_perm',
            field=models.ManyToManyField(to='SecureWitness.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='report',
            field=models.ForeignKey(to='SecureWitness.Report'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='authorId',
            field=models.ForeignKey(to='SecureWitness.UserProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='groupId',
            field=models.ForeignKey(to='SecureWitness.Group'),
            preserve_default=True,
        ),
    ]
