# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0003_player_bye_week'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['number']},
        ),
    ]
