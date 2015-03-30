# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecureWitness', '0002_auto_20150326_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='dateOfIncident',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='detailsDesc',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='keywords',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='locationOfIncident',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='shortDesc',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='timestamp',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
    ]
