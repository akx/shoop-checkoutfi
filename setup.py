import os

import setuptools

try:
    import shoop_setup_utils
except ImportError:
    shoop_setup_utils = None


VERSION = '0.3.2'

TOPDIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(TOPDIR, 'shoop_checkoutfi', '_version.py')

if __name__ == '__main__':
    if shoop_setup_utils:
        shoop_setup_utils.write_version_to_file(VERSION, VERSION_FILE)

    setuptools.setup(
        name="shoop-checkoutfi",
        version=VERSION,
        description="Shoop Checkout.fi Integration",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_checkoutfi=shoop_checkoutfi"},
        cmdclass=(shoop_setup_utils.COMMANDS if shoop_setup_utils else {}),
        install_requires=[
            'shoop>=3.0.0.post0.dev233,<5.0',
        ],
    )
