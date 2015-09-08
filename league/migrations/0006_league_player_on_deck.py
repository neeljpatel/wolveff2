# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0005_auto_20150908_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='player_on_deck',
            field=models.ForeignKey(related_name=b'player_on_deck', to='league.Player', null=True),
            preserve_default=True,
        ),
    ]
