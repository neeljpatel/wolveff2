# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0002_auto_20140903_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bye_week',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
