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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('file', models.FileField(upload_to='SecureWitness/', null=True, default='', blank=True)),
                ('fileType', models.CharField(default='', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('name', models.CharField(serialize=False, primary_key=True, max_length=200)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('file', models.OneToOneField(primary_key=True, to='SecureWitness.File', serialize=False)),
                ('key', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(default='', max_length=300)),
                ('authorName', models.CharField(default='', blank=True, max_length=30)),
                ('folder', models.IntegerField(blank=True, default='0')),
                ('user_perm', models.TextField(blank=True, default='')),
                ('access_type', models.BooleanField(default=False)),
                ('timestamp', models.TextField(blank=True, default='')),
                ('shortDesc', models.TextField(blank=True, default='')),
                ('detailsDesc', models.TextField(blank=True, default='')),
                ('dateOfIncident', models.TextField(null=True, blank=True, default='')),
                ('locationOfIncident', models.TextField(null=True, blank=True, default='')),
                ('keywords', models.TextField(null=True, blank=True, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
            field=models.ForeignKey(blank=True, to='SecureWitness.UserProfile'),
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
    ]
