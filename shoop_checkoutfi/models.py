# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import unicodedata

from django.contrib import messages
from django.db import models
from django.forms import CharField, Form, HiddenInput
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from shoop.core.models import PaymentProcessor, ServiceChoice
from shoop.utils.excs import Problem
from shoop_checkoutfi.checkoutfi import Checkout, Contact, Payment


TEMPLATE = """
<html>
<body>
    <form action="https://payment.checkout.fi/" method="post">
        %(form)s
        <input type="submit" value="Continue to Checkout.fi">
    </form>
    <script>setTimeout(function(){document.forms[0].submit();}, 50);</script>
</body>
</html>
"""


def flatten_unicode(string):
    string = force_text(string)
    return force_text(unicodedata.normalize("NFKD", string).encode("ascii", "ignore"))


class CheckoutFiPaymentProcessor(PaymentProcessor):
    merchant_id = models.CharField(verbose_name="Merchant ID", max_length=128)
    merchant_secret = models.CharField(verbose_name="Merchant Secret", max_length=128)

    def get_service_choices(self):
        return [
            ServiceChoice('checkoutfi', _("Checkout.fi"))
        ]

    def _get_checkout_object(self, service):
        return Checkout(
            merchant_id=self.merchant_id,
            merchant_secret=self.merchant_secret,
        )

    def process_payment_return_request(self, service, order, request):
        checkout = self._get_checkout_object(service)
        fields = {
            "version": request.REQUEST.get("VERSION"),
            "order_number": request.REQUEST.get("STAMP"),
            "order_reference": request.REQUEST.get("REFERENCE"),
            "payment": request.REQUEST.get("PAYMENT"),
            "status": request.REQUEST.get("STATUS"),
            "algorithm": request.REQUEST.get("ALGORITHM"),
            "mac": request.REQUEST.get("MAC"),
        }

        if not all(fields.values()):
            messages.warning(request, u"Arvoja puuttuu.")
            return

        status = int(fields["status"])

        if status < 0:
            messages.warning(request, u"Peruit maksamisen. Yritä uudestaan.")
            return

        # these are approved statuses
        if status in (2, 3, 5, 6, 8, 9, 10):
            if checkout.validate_payment_return(**fields):
                payment_id = fields["payment"]
                order.create_payment(
                    order.taxful_total_price,
                    payment_identifier="Checkout.fi %s" % payment_id,
                    description="Checkout.fi %s (ref %s)" % (payment_id, fields["order_reference"])
                )
            else:
                messages.warning(request, u"Maksun validointi epäonnistui.")
            return

        raise Problem("Unknown return code %s" % status)

    def get_payment_process_response(self, service, order, urls):
        address = order.billing_address
        payment = Payment(
            order_number=order.identifier,
            reference_number=order.reference_number[:20],
            amount=str(int(order.taxful_total_price * 100)),
            delivery_date=(order.order_date.date() + datetime.timedelta(1)).strftime("%Y%m%d"),
            return_url=urls.return_url,
            delayed_url=urls.return_url,
            cancel_url=urls.cancel_url,
            message=force_text(order),
            contact=Contact(
                first_name=flatten_unicode(address.first_name),
                last_name=flatten_unicode(address.last_name),
                email=flatten_unicode(address.email),
                phone=flatten_unicode(address.phone),
                address=flatten_unicode(address.street),
                postcode=address.postal_code,
                postoffice=flatten_unicode(address.city),
                country=address.country.alpha3
            )
        )
        form = Form()
        for key, value in self._get_checkout_object(service).get_offsite_button_data(payment).items():
            form.fields[key] = CharField(initial=value, widget=HiddenInput)
        html = TEMPLATE % {"form": form}
        return HttpResponse(html)
