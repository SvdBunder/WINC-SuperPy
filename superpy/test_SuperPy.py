import classes as SPclass


purchase_1 = SPclass.Product(
    product_name="orange", amount=8, price_unit=0.50, expiration_date="2022-09-12"
)
purchase_1.buy()

purchase_2 = SPclass.Product(
    product_name="pear", amount=12, price_unit=0.25, expiration_date="2022-09-12"
)
purchase_2.buy()

purchase_3 = SPclass.Product(
    product_name="milk", amount=5, price_unit=1.50, expiration_date="2022-09-22"
)
purchase_3.buy()

purchase_4 = SPclass.Product(
    product_name="orange", amount=5, price_unit=0.55, expiration_date="2022-09-17"
)
purchase_4.buy()

purchase_5 = SPclass.Product(
    product_name="chocolate", amount=28, price_unit=2.60, expiration_date="2022-12-12"
)
purchase_5.buy()

purchase_6 = SPclass.Product(
    product_name="orange", amount=9, price_unit=0.70, expiration_date="2022-10-01"
)
purchase_6.buy()

purchase_7 = SPclass.Product(
    product_name="milk", amount=18, price_unit=1.75, expiration_date="2022-10-30"
)
purchase_7.buy()

purchase_8 = SPclass.Product(
    product_name="pineapple", amount=4, price_unit=1.90, expiration_date="2022-09-30"
)
purchase_8.buy()
