try:
    from ._version import __version__
except ImportError:
    __version__ = 'dev'

default_app_config = "shoop_checkoutfi.apps.CheckoutFiConfig"
