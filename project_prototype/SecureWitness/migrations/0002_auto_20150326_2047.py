# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='author',
        ),
        migrations.RemoveField(
            model_name='file',
            name='folder',
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='practice/%Y/%m/%d', default='foo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='group_perm',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='user_perm',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
    ]
