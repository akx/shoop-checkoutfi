# -*- coding: utf-8 -*-
from django import forms
from shuup.admin.forms import ShuupAdminForm
from shuup.admin.modules.service_providers.wizard_form_defs import \
    ServiceWizardFormDef
from shuup.admin.modules.service_providers.wizard_forms import \
    ServiceWizardForm

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
    def __init__(self, **kwargs):
        super(CheckoutFiWizardForm, self).__init__(**kwargs)
        if not self.provider:
            return
        service = self.get_payment_method()
        if not service:
            return
        self.fields["service_name"].initial = service.name
        self.fields["merchant_id"].initial = self.provider.merchant_id
        self.fields["merchant_secret"].initial = self.provider.merchant_secret


class CheckoutFiWizardFormDef(ServiceWizardFormDef):
    def __init__(self, request):
        self.request = request
        super(CheckoutFiWizardFormDef, self).__init__(
            name="checkoutfi",
            form_class=CheckoutFiWizardForm,
            template_name="shuup/checkoutfi/wizard_form.jinja",
            request=request
        )

    def visible(self):
        shop = self.request.shop
        return not shop or not shop.contact_address or shop.contact_address.country == "FI"
