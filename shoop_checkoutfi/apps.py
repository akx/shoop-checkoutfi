# -*- coding: utf-8 -*-
from shoop.apps import AppConfig


class CheckoutFiConfig(AppConfig):
    name = "shoop_checkoutfi"
    provides = {
        "service_provider_admin_form": [
            "shoop_checkoutfi.admin_forms:CheckoutFiAdminForm"
        ]
    }
