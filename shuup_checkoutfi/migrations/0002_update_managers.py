# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-22 23:00
from __future__ import unicode_literals

from django.db import migrations

from shuup.utils.migrations import get_managers_for_migration


class Migration(migrations.Migration):

    dependencies = [
        ('shuup_checkoutfi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkoutfipaymentprocessor',
            options={'verbose_name': 'Checkout.fi payment processor'},
        ),
        migrations.AlterModelManagers(
            name='checkoutfipaymentprocessor',
            managers=get_managers_for_migration(),
        ),
    ]
