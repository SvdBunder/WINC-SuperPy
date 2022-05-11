import SuperPy_functions_time as SPtime
import SuperPy_functions_stock as SPstock


SPstock.check_files()
SPtime.save_time()

SPstock.buy_product(
    product_name="orange", amount=8, price_unit=0.50, expiration_date="2022-05-12"
)
SPstock.buy_product(
    product_name="orange",
    buy_date="2022-05-07",
    amount=5,
    price_unit=0.55,
    expiration_date="2022-05-17",
)
SPstock.buy_product(
    product_name="pear", amount=12, price_unit=0.40, expiration_date="2022-05-12"
)
SPstock.buy_product(
    product_name="milk", amount=10, price_unit=1.50, expiration_date="2022-06-12"
)
SPstock.buy_product(
    product_name="chocolate", amount=30, price_unit=2.80, expiration_date="2022-08-20"
)
SPstock.buy_product(
    product_name="orange",
    buy_date="2022-05-14",
    amount=9,
    price_unit=0.70,
    expiration_date="2022-06-01",
)
SPstock.buy_product(
    product_name="milk",
    buy_date="2022-05-07",
    amount=3,
    price_unit=1.25,
    expiration_date="2022-06-30",
)
