# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0003_auto_20150330_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='dateOfIncident',
            field=models.TextField(null=True, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='keywords',
            field=models.TextField(null=True, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='locationOfIncident',
            field=models.TextField(null=True, default='', blank=True),
            preserve_default=True,
        ),
    ]
