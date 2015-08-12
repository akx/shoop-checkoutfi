# -*- coding: utf-8 -*-
"""
    checkout
    ~~~~~~~~~~~~

    Python wrapper for the Checkout Finland API.

    Copyright (c) 2014 by Tuomas Blomqvist.
    Copyright (c) 2013 by Janne Vanhala.

    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * The names of the contributors may not be used to endorse or
      promote products derived from this software without specific
      prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import hashlib
import hmac
import xml.etree.ElementTree as ET
import requests

__version__ = '0.2.0'

try:
    text_type = unicode  # This is Py2
except NameError:  # Must be Py3
    text_type = str


def join_as_bytes(joiner, bits, encoding="ascii"):
    joined_unicode = text_type(joiner).join(text_type(bit) for bit in bits)
    return joined_unicode.encode(encoding)


class CheckoutException(Exception):
    """This exception is raised when the request made to the Checkout API
    is invalid, or some other error occurs in the usage of the API."""

    def __init__(self, message):
        #: An error description of the error in chosen localization. This error
        #: description is not meant to be displayed to the end-user.
        self.message = message


class Contact(object):
    """This class represents the payer of a payment.
    Contact details are optional """

    def __init__(self, **options):
        #: Payer's first name.
        self.first_name = options.get('first_name', '')[0:40]

        #: Payer's surname.
        self.last_name = options.get('last_name', '')[0:40]

        #: Payer's email address.
        self.email = options.get('email', '')[0:200]

        #: Payer's telephone number.
        self.phone = options.get('phone', '')[0:30]

        #: Payer's street address.
        self.address = options.get('address', '')[0:40]

        #: Payer's postal code.
        self.postcode = options.get('postcode', '')[0:14]

        #: Payer's post office.
        self.postoffice = options.get('postoffice', '')[0:18]

        #: Payer's country. 3-letter ISO code.
        self.country = options.get('country', '')[0:3]

    @property
    def dict(self):
        """Dict of this contact in fields specified by Checkout API and clipped accordingly."""
        return {
            'PHONE': self.phone,
            'EMAIL': self.email,
            'FIRSTNAME': self.first_name,
            'FAMILYNAME': self.last_name,
            'ADDRESS': self.address,
            'POSTCODE': self.postcode,
            'POSTOFFICE': self.postoffice,
            'COUNTRY': self.country
        }


class Payment(object):
    def __init__(self, order_number, reference_number, amount, delivery_date, return_url, cancel_url, **options):
        #: Order number is a string of characters identifying the customer's
        #: purchase and the used webshop software creates it. Mandatory.
        if len(order_number) > 20:
            raise CheckoutException("order_number over maximum allowed 20 characters")
        else:
            self.order_number = order_number

        #: Reference number is sent to bank by default and is automatically
        #: created.  In those payment methods that are used as an interface,
        #: this field can contain own reference number, which is sent to the
        #: bank service instead of the automatically generated reference
        #: number. Mandatory.
        if len(reference_number) > 20:
            raise CheckoutException("reference_number over maximum allowed 20 characters")
        else:
            self.reference_number = reference_number

        #: Order amount in cents. Mandatory.
        if len(amount) > 8:
            raise CheckoutException("amount over maximum allowed 8 characters")
        else:
            self.amount = amount

        #: Delivery date of order in format YYYYMMDD. Mandatory
        if len(delivery_date) > 8:
            raise CheckoutException("delivery_date over maximum allowed 8 characters")
        else:
            self.delivery_date = delivery_date

        #: Any data about the order in text format can be sent to the payment
        #: system. They are shown in the Merchant's Panel in payment details. Optional.
        self.message = options.get('message', '')[0:1000]

        #: Payment currency.  Value must EUR for the Finnish banks, otherwise
        #: the payment will not be accepted. Mandatory, defaults to 'EUR'.
        self.currency = options.get('currency', 'EUR')

        #: Language defines default language for the payment method
        #: selection page. Optional, 2-letter ISO code.
        self.language = options.get('language', 'FI')

        #: Contact object for the Payment. Optional, if supplied with None blank contact is used.
        self.contact = options.get('contact', Contact())

        #: Payment content. "1" for normal content and "10" for adult content. Mandatory, default 1.
        self.content = options.get('content', '1')[0:2]

        #: URL to which user is redirected after a successful payment. Mandatory.
        if len(return_url) > 300:
            raise CheckoutException("return_url over maximum allowed 300 characters")
        else:
            self.return_url = return_url

        #: URL to which user is redirected after a cancelled or failed payment. Mandatory.
        if len(cancel_url) > 300:
            raise CheckoutException("cancel_url over maximum allowed 300 characters")
        else:
            self.cancel_url = cancel_url

        #: URL to which user is directed, if the payment is pending.
        #: After the actual payment, the payment acknowledged as received by Checkout
        #: with fetching this URL along with same parameters as used in normal return_url.
        #: Optional.
        self.delayed_url = options.get('delayed_url', '')
        if len(self.delayed_url) > 300:
            raise CheckoutException("delayed_url over maximum allowed 300 characters")

        #: URL requested when the payment is marked as rejected.  The URL is
        #: requested with the same GET parameters as return address when the
        #: payment is made. Optional.
        self.reject_url = options.get('reject_url', '')
        if len(self.reject_url) > 300:
            raise CheckoutException("reject_url over maximum allowed 300 characters")

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if value != 'EUR':
            raise CheckoutException("Currently EUR is the only supported currency.")
        self._currency = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        if value not in ('FI', 'SE', 'EN'):
            raise CheckoutException("Given language is not supported: %r" % value)
        self._language = value

    @property
    def dict(self):
        returndict = {
            'VERSION': "0001",  #: Version of the API.
            'STAMP': self.order_number,
            'AMOUNT': self.amount,
            'REFERENCE': self.reference_number,
            'MESSAGE': self.message,
            'LANGUAGE': self.language,
            'RETURN': self.return_url,
            'CANCEL': self.cancel_url,
            'REJECT': self.reject_url,
            'DELAYED': self.delayed_url,
            'CURRENCY': self.currency,
            'CONTENT': self.content,
            'TYPE': "0",  #: Static field.
            'ALGORITHM': "3",  #: Return AUTHCODE algorithm, "3" for HMAC-SHA256.
            'DELIVERY_DATE': self.delivery_date
        }
        #: Merge with Contact values
        returndict.update(self.contact.dict)
        return returndict


class Checkout(object):
    SERVICE_URL = "https://payment.checkout.fi/"

    def __init__(self, merchant_id='375917',
                 merchant_secret='SAIPPUAKAUPPIAS'):
        """
        Initialize Checkout with your own merchant id and merchant secret.

        :param merchant_id: Mercant ID is given to you by Checkout
            when you make the contract. Default is the test merchant_id.
        :param merchant_secret: Merchant secret is given to you by Checkout.
            Default is the test merchant_secret.
        """
        self.merchant_id = merchant_id
        self.merchant_secret = merchant_secret
        self.session = requests.Session()

    def get_onsite_button_data(self, payment):
        """
        Creates a new payment and returns a `list` with the following data for each payment method:
        { 'bank': bankname, 'url': posturl, 'icon': iconurl, formfields: {} }

        :param payment: a `Payment` object
        """
        postdict = payment.dict
        postdict['MERCHANT'] = self.merchant_id
        postdict['DEVICE'] = "10"  #: "10" to get XML data for payment methods back
        postdict['MAC'] = self._calculate_payment_md5(postdict, self.merchant_secret)
        response = self.session.post(self.SERVICE_URL, data=postdict)
        return self.parse_xml_response(response.content)

    def get_offsite_button_data(self, payment):
        """
        Returns form fields for off-page payment where user is sent to checkout.fi and shown
        all the payment options there instead of showing them onsite.

        :param payment: a `Payment` object
        """
        paymentdict = payment.dict
        paymentdict['MERCHANT'] = self.merchant_id
        paymentdict['DEVICE'] = "1"  #: "1" to get payment method selection form from Checkout.fi
        paymentdict['MAC'] = self._calculate_payment_md5(paymentdict, self.merchant_secret)
        return paymentdict

    def parse_xml_response(self, xmlraw):
        """
        Parses XML-response for onsite payment method

        :param xmlraw: Raw XML data returned by checkout.fi
        """
        payment_list = []
        XML = ET.fromstring(xmlraw)
        banks = XML.findall(".//payment/banks/*")
        for bank in banks:
            bankdict = dict(bank.items())
            fielddict = {}
            for fieldname in bank:
                fielddict[fieldname.tag] = fieldname.text
            bankdict["fields"] = fielddict
            payment_list.append(bankdict)
        return payment_list

    def _calculate_payment_md5(self, params, merchant_secret):
        fields = [params["VERSION"], params["STAMP"], params["AMOUNT"], params["REFERENCE"],
                  params["MESSAGE"], params["LANGUAGE"], params["MERCHANT"], params["RETURN"],
                  params["CANCEL"], params["REJECT"], params["DELAYED"], params["COUNTRY"],
                  params["CURRENCY"], params["DEVICE"], params["CONTENT"], params["TYPE"],
                  params["ALGORITHM"], params["DELIVERY_DATE"], params["FIRSTNAME"], params["FAMILYNAME"],
                  params["ADDRESS"], params["POSTCODE"], params["POSTOFFICE"], merchant_secret]
        base = join_as_bytes("+", fields)
        return hashlib.md5(base).hexdigest().upper()

    def validate_payment_return(self, mac, version, order_number, order_reference, payment, status, algorithm):
        """
        Validates parameters sent by Checkout Finland to the success/cancel URL or
        delayed/reject URL after a payment. The parameters must be validated
        in order to avoid hacking attempts to confirm payment. Returns `True`
        when the parameters are valid, and `False` otherwise.

        :param mac: A hash value calculated by payment system and sent to return url.
        :param version: Payment version number. GET parameter 'VERSION'.
        :param order_number: The same order number that was previously sent to
            the payment system. GET parameter 'STAMP'.
        :param order_reference: The same order reference that was previously sent
            to the payment system. GET parameter 'REFERENCE'.
        :param payment: A payment identified produced by Checkout Finland used
            for calculating the hash.
        :param status: Payment status code, which is part of payment
            confirmation. '2'/'5'/'6'/'8'/'9'/'10' = success. '3' = delayed. '-1' = cancelled.
            '7' = manual activation required. GET parameter 'STATUS'.
            Specified here: http://checkout.fi/uploads/sopimukset/Checkout_1_4_rajapinta_api-v1.7.pdf
        :param status: Payment return algorithm version. This library uses version 3.
            GET parameter 'ALGORITHM'.
        """
        fields = [version, order_number, order_reference, payment, status, algorithm]
        base = join_as_bytes("&", fields)
        key = text_type(self.merchant_secret).encode("ascii")
        return mac == hmac.new(key, base, hashlib.sha256).hexdigest().upper()
