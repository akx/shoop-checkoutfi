# -*- coding: utf-8 -*-
from django import forms

from shuup.admin.forms import ShuupAdminForm

from .models import CheckoutFiPaymentProcessor


class CheckoutFiAdminForm(ShuupAdminForm):
    class Meta:
        model = CheckoutFiPaymentProcessor
        fields = '__all__'
        widgets = {
            'secret_key': forms.PasswordInput(render_value=True),
            'publishable_key': forms.PasswordInput(render_value=True),
        }
