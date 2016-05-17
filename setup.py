import setuptools

try:
    import shoop_setup_utils
except ImportError:
    shoop_setup_utils = None


if __name__ == '__main__':
    setuptools.setup(
        name="shoop-checkoutfi",
        version="0.2",
        description="Shoop Checkout.fi Integration",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_checkoutfi=shoop_checkoutfi"},
        cmdclass=(shoop_setup_utils.COMMANDS if shoop_setup_utils else {}),
        install_requires=[
            'shoop>=3.0.0.post0.dev233,<5.0',
        ],
    )
