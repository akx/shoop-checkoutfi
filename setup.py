import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name="shoop-checkoutfi",
        version="0.1",
        description="Shoop Checkout.fi Integration",
        packages=["shoop_checkoutfi"],
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_checkoutfi=shoop_checkoutfi"}
    )
