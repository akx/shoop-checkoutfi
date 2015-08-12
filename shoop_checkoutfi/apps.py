# -*- coding: utf-8 -*-
from shoop.apps import AppConfig


class CheckoutFiConfig(AppConfig):
    name = "shoop_checkoutfi"
    provides = {
        "payment_method_module": [
            "shoop_checkoutfi.payment_method:CheckoutFiPaymentMethodModule"
        ]
    }
