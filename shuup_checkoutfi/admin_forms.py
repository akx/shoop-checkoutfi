# -*- coding: utf-8 -*-
from django import forms
from shuup.admin.forms import ShuupAdminForm
from shuup.admin.modules.service_providers.forms import (ServiceWizardForm,
                                                         ServiceWizardFormDef)
from shuup.core.models import Shop

from .models import CheckoutFiPaymentProcessor


class CheckoutFiAdminForm(ShuupAdminForm):
    class Meta:
        model = CheckoutFiPaymentProcessor
        exclude = []
        widgets = {
            'merchant_id': forms.PasswordInput(render_value=True),
            'merchant_secret': forms.PasswordInput(render_value=True),
        }


class CheckoutFiWizardForm(CheckoutFiAdminForm, ServiceWizardForm):
    pass


class CheckoutFiWizardFormDef(ServiceWizardFormDef):
    def __init__(self):
        super(CheckoutFiWizardFormDef, self).__init__(
            name="checkoutfi",
            form_class=CheckoutFiWizardForm,
            template_name="shuup/checkoutfi/wizard_form.jinja"
        )

    def visible(self):
        shop = Shop.objects.first()
        return not shop or not shop.contact_address or shop.contact_address.country == "FI"
