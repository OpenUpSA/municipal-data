# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0040_auto_20210222_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='agedcreditoritemsv1',
            name='id',
            field=models.IntegerField(null=True),
        ),
    ]
