# -*- coding: utf-8 -*-
from django import forms

from shoop.admin.forms import ShoopAdminForm

from .models import CheckoutFiPaymentProcessor


class CheckoutFiAdminForm(ShoopAdminForm):
    class Meta:
        model = CheckoutFiPaymentProcessor
        fields = '__all__'
        widgets = {
            'secret_key': forms.PasswordInput(render_value=True),
            'publishable_key': forms.PasswordInput(render_value=True),
        }
