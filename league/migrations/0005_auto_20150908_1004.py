# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0004_auto_20140903_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplatePlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=5)),
                ('team', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='player',
            name='bye_week',
        ),
        migrations.AddField(
            model_name='player',
            name='is_garbage',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
