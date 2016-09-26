import os

import setuptools

try:
    import shuup_setup_utils
except ImportError:
    shuup_setup_utils = None


VERSION = '0.5.1'

TOPDIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(TOPDIR, 'shuup_checkoutfi', '_version.py')

if __name__ == '__main__':
    if shuup_setup_utils:
        shuup_setup_utils.write_version_to_file(VERSION, VERSION_FILE)

    setuptools.setup(
        name="shuup-checkoutfi",
        version=VERSION,
        description="Shuup Checkout.fi Integration",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={"shuup.addon": "shuup_checkoutfi=shuup_checkoutfi"},
        cmdclass=(shuup_setup_utils.COMMANDS if shuup_setup_utils else {}),
        install_requires=[
            'shuup>=0.4',
        ],
    )
