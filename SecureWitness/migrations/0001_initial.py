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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('comment', models.TextField(default='', blank=True)),
                ('authorName', models.CharField(default='', blank=True, max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('file', models.FileField(null=True, default='', blank=True, upload_to='SecureWitness/')),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('file', models.FileField(upload_to='SecureWitness/', default='', blank=True, null=True)),
>>>>>>> c4d9503792c56171e3f0f0f705d9458b0d585fb9
                ('fileType', models.CharField(default='', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> c4d9503792c56171e3f0f0f705d9458b0d585fb9
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
<<<<<<< HEAD
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
=======
                ('name', models.CharField(primary_key=True, serialize=False, max_length=200)),
>>>>>>> c4d9503792c56171e3f0f0f705d9458b0d585fb9
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
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> c4d9503792c56171e3f0f0f705d9458b0d585fb9
                ('title', models.CharField(default='', max_length=300)),
                ('authorName', models.CharField(default='', blank=True, max_length=30)),
                ('folder', models.IntegerField(default='0', blank=True)),
                ('user_perm', models.TextField(default='', blank=True)),
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
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> c4d9503792c56171e3f0f0f705d9458b0d585fb9
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
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> c4d9503792c56171e3f0f0f705d9458b0d585fb9
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
