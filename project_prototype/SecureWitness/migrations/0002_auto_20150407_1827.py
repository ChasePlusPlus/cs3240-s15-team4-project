# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='author',
            new_name='authorId',
        ),
        migrations.RemoveField(
            model_name='report',
            name='files',
        ),
        migrations.AddField(
            model_name='report',
            name='authorName',
            field=models.CharField(max_length=30, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='file1',
            field=models.FileField(null=True, default='', upload_to='SecureWitness/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='file2',
            field=models.FileField(null=True, default='', upload_to='SecureWitness/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='file3',
            field=models.FileField(null=True, default='', upload_to='SecureWitness/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='file4',
            field=models.FileField(null=True, default='', upload_to='SecureWitness/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='file5',
            field=models.FileField(null=True, default='', upload_to='SecureWitness/', blank=True),
            preserve_default=True,
        ),
    ]
