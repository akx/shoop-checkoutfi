.. image:: https://travis-ci.org/shuup/shuup-checkoutfi.svg?branch=master
  :target: https://travis-ci.org/shuup/shuup-checkoutfi

.. image:: https://codecov.io/gh/shuup/shuup-checkoutfi/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/shuup/shuup-checkoutfi

.. image:: https://img.shields.io/pypi/v/shuup-checkoutfi.svg
  :alt: PyPI
  :target: https://pypi.org/project/shuup-checkoutfi/

shuup-checkoutfi
================

A simple Checkout.fi_ payment module for the Shuup_ e-commerce platform.

.. _Checkout.fi: http://www.checkout.fi/
.. _Shuup: http://github.com/shuup/shuup

Usage
-----

* Install the package (should be installable via
  ``pip install <this_dir>``)
* Add ``shuup_checkoutfi`` to your ``INSTALLED_APPS``
* Restart your application server
* Create a Checkout.fi payment processor in Shop Admin with proper
  values for Merchant ID and Merchant Secret.
* Create a new payment method for the payment processor.
* All done! Payments with the payment method will go through
  Checkout.fi.

Testing values
--------------

**Don't use these in production, silly.**

* Merchant ID: ``375917``
* Merchant Secret: ``SAIPPUAKAUPPIAS``

Running tests
-------------

You can run tests with `py.test <http://pytest.org/>`_.

Requirements for running tests:

* Your virtualenv needs to have Shuup installed.

* Project root must be in the Python path.  This can be done with:

  .. code:: sh

     pip install -e .

To run tests, use command:

.. code:: sh

   py.test -v shuup_checkoutfi_tests

Third-Party Licenses
--------------------

This package includes a vendored version of the python-checkout_ module,
which is BSD licensed.

.. _python-checkout: https://github.com/tuomasb/python-checkout

License
-------

Copyright (c) 2016 Shoop Commerce Ltd.
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
