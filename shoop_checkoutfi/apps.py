# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from shoop.apps import AppConfig


class CheckoutFiConfig(AppConfig):
    name = "shoop_checkoutfi"
    verbose_name = _("Checkout.fi Payments Addon")
    provides = {
        "service_provider_admin_form": [
            "shoop_checkoutfi.admin_forms:CheckoutFiAdminForm"
        ]
    }
