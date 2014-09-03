# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='league',
            field=models.ForeignKey(default=-1, to='league.League'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='number',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(default=None, max_length=200, choices=[(b'qb', b'quarterback'), (b'rb', b'running back'), (b'wr', b'wide receiver'), (b'te', b'tight end'), (b'k', b'kicker'), (b'def', b'defense')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='cost',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='roster',
            field=models.ForeignKey(blank=True, to='league.Roster', null=True),
        ),
    ]
