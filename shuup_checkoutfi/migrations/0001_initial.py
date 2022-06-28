# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shuup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckoutFiPaymentProcessor',
            fields=[
                ('paymentprocessor_ptr', models.OneToOneField(parent_link=True, to='shuup.PaymentProcessor', auto_created=True, serialize=False, primary_key=True)),
                ('merchant_id', models.CharField(max_length=128, verbose_name='Merchant ID')),
                ('merchant_secret', models.CharField(max_length=128, verbose_name='Merchant Secret')),
            ],
            options={
                'abstract': False,
            },
            bases=('shuup.paymentprocessor',),
        ),
    ]
