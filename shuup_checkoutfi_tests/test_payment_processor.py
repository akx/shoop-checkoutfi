# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

import mock
import pytest
from django.test import override_settings
from shuup.admin.views.wizard import WizardView
from shuup.core.models import (
    CustomPaymentProcessor, PaymentMethod, PaymentStatus,
    ServiceBehaviorComponent, StaffOnlyBehaviorComponent
)
from shuup.core.pricing import TaxfulPrice
from shuup.testing import factories
from shuup.testing.factories import (
    create_order_with_product, get_default_product, get_default_shop,
    get_default_supplier, get_default_tax_class
)
from shuup.testing.utils import apply_request_middleware

from shuup_checkoutfi.checkoutfi import Checkout
from shuup_checkoutfi.models import CheckoutFiPaymentProcessor


@pytest.mark.django_db
def test_payment_processor(rf):
    shop = get_default_shop()
    product = get_default_product()
    supplier = get_default_supplier()
    choice_identifier = "checkoutfi"
    processor = CheckoutFiPaymentProcessor.objects.create(merchant_id="1", merchant_secret="2")
    payment_method = PaymentMethod.objects.create(
        shop=shop,
        payment_processor=processor,
        choice_identifier=choice_identifier,
        tax_class=get_default_tax_class()
    )
    order = create_order_with_product(
        product=product,
        supplier=supplier,
        quantity=1,
        taxless_base_unit_price=Decimal('5.55'),
        shop=shop
    )
    order.taxful_total_price = TaxfulPrice(Decimal('5.55'), 'EUR')
    order.payment_method = payment_method
    order.save()

    request = rf.get("/", data={
        "VERSION": "1",
        "STAMP": "2",
        "REFERENCE": "3",
        "PAYMENT": "4",
        "STATUS": "5",
        "ALGORITHM": "6",
        "MAC": "7"
    })
    assert order.payment_status == PaymentStatus.NOT_PAID

    with mock.patch.object(Checkout, "validate_payment_return", return_value=True):
        processor.process_payment_return_request(choice_identifier, order, request)
        order.refresh_from_db()
        assert order.payment_status == PaymentStatus.FULLY_PAID

        processor.process_payment_return_request(choice_identifier, order, request)
        order.refresh_from_db()
        assert order.payment_status == PaymentStatus.FULLY_PAID
