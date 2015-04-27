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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('comment', models.TextField(default='', blank=True)),
                ('authorName', models.CharField(default='', blank=True, max_length=30)),
                ('timestamp', models.TextField(default='', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(default='', upload_to='', blank=True, null=True)),
                ('fileType', models.CharField(default='', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('file', models.OneToOneField(serialize=False, primary_key=True, to='SecureWitness.File')),
                ('key', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300)),
                ('authorName', models.CharField(default='', blank=True, max_length=30)),
                ('folder', models.IntegerField(default='0', blank=True)),
                ('user_perm', models.TextField(default='', blank=True)),
                ('dechunker', models.CharField(default='', blank=True, max_length=256)),
                ('iv', models.CharField(default='', blank=True, max_length=256)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
        migrations.AddField(
            model_name='comments',
            name='authorId',
            field=models.ForeignKey(blank=True, to='SecureWitness.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='groupId',
            field=models.ForeignKey(to='SecureWitness.Group'),
            preserve_default=True,
        ),
    ]
