# -- encoding: UTF-8 --
from __future__ import unicode_literals
from .checkoutfi import Checkout, Payment, Contact
from django.contrib import messages
from django.forms import Form, CharField, HiddenInput
from django.http.response import HttpResponse
from django.utils.encoding import force_text
from shoop.core.methods.base import BasePaymentMethodModule
from shoop.utils.excs import Problem
import datetime
import unicodedata

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


class CheckoutFiPaymentMethodModule(BasePaymentMethodModule):
    identifier = "checkoutfi"
    name = "Checkout.fi"
    option_fields = BasePaymentMethodModule.option_fields + [
        ("merchant_id", CharField(label="Merchant ID", required=True)),
        ("merchant_secret", CharField(label="Merchant Secret", required=True))
    ]

    def _get_checkout_object(self):
        options = self.get_options()
        return Checkout(
            merchant_id=options["merchant_id"],
            merchant_secret=options["merchant_secret"],
        )

    def process_payment_return_request(self, order, request):
        checkout = self._get_checkout_object()
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

    def get_payment_process_response(self, order, urls):
        address = order.billing_address
        payment = Payment(
            order_number=order.identifier,
            reference_number=order.reference_number[:20],
            amount=str(int(order.taxful_total_price * 100)),
            delivery_date=(order.order_date.date() + datetime.timedelta(1)).strftime("%Y%m%d"),
            return_url=urls["return"],
            delayed_url=urls["return"],
            cancel_url=urls["cancel"],
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
        for key, value in self._get_checkout_object().get_offsite_button_data(payment).items():
            form.fields[key] = CharField(initial=value, widget=HiddenInput)
        html = TEMPLATE % {"form": form}
        return HttpResponse(html)
