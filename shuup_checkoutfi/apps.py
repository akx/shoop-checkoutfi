# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from shuup.apps import AppConfig


class CheckoutFiConfig(AppConfig):
    name = "shuup_checkoutfi"
    verbose_name = _("Checkout.fi Payments Addon")
    provides = {
        "service_provider_admin_form": [
            "shuup_checkoutfi.admin_forms:CheckoutFiAdminForm"
        ],
        "payment_processor_wizard_form_def": [
            "shuup_checkoutfi.admin_forms:CheckoutFiWizardFormDef"
        ]
    }
