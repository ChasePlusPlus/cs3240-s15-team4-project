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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('comment', models.TextField(blank=True, default='')),
                ('authorName', models.CharField(blank=True, max_length=30, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='SecureWitness/', default='')),
                ('fileType', models.CharField(max_length=200, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('file', models.OneToOneField(serialize=False, to='SecureWitness.File', primary_key=True)),
                ('key', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=300, default='')),
                ('authorName', models.CharField(blank=True, max_length=30, default='')),
                ('folder', models.IntegerField(blank=True, default='0')),
                ('user_perm', models.TextField(blank=True, default='')),
                ('dechunker', models.CharField(blank=True, max_length=256, default='')),
                ('iv', models.CharField(blank=True, max_length=256, default='')),
                ('access_type', models.BooleanField(default=False)),
                ('timestamp', models.TextField(blank=True, default='')),
                ('shortDesc', models.TextField(blank=True, default='')),
                ('detailsDesc', models.TextField(blank=True, default='')),
                ('dateOfIncident', models.TextField(blank=True, null=True, default='')),
                ('locationOfIncident', models.TextField(blank=True, null=True, default='')),
                ('keywords', models.TextField(blank=True, null=True, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
