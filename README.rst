shoop-checkoutfi
================

A simple Checkout.fi_ payment module for the Shoop_ e-commerce platform.

.. _Checkout.fi: http://www.checkout.fi/
.. _Shoop: http://github.com/shoopio/shoop

Usage
-----

* Install the package (should be installable via
  ``pip install <this_dir>``)
* Add ``shoop_checkoutfi`` to your ``INSTALLED_APPS``
* Restart your application server
* Set "Checkout.fi" as the payment method module for a payment method.
  Save changes.
* Set the merchant ID and merchant secret.
* All done! Payments with the payment method will go through
  Checkout.fi.

Testing values
--------------

**Don't use these in production, silly.**

* Merchant ID: ``375917``
* Merchant Secret: ``SAIPPUAKAUPPIAS``

Third-Party Licenses
--------------------

This package includes a vendored version of the python-checkout_ module,
which is BSD licensed.

.. _python-checkout: https://github.com/tuomasb/python-checkout

License
-------

Copyright (c) 2016 Shoop Ltd.
Copyright (c) 2015 Aarni Koskela

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
