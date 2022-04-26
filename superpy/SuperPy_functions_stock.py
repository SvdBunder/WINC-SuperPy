# imports
import csv, os.path
from datetime import date, datetime

# functions regarding registering stock movements - to be called by SuperPy.py


def check_files():
    if os.path.isfile("purchases.csv"):
        print("Purchases file: OK")
    else:
        with open("purchases.csv", mode="w") as purchases_file:
            fieldnames = [
                "ID",
                "product_name",
                "buy_date",
                "buy_amount",
                "buy_price_unit",
                "expiration_date",
            ]
            writer = csv.DictWriter(purchases_file, fieldnames=fieldnames)

            writer.writeheader()
            print("Purchases file created")

    if os.path.isfile("sales.csv"):
        print("Sales file: OK")
    else:
        with open("sales.csv", mode="w") as sales_file:
            fieldnames = [
                "ID",
                "buy_ID",
                "product_name",
                "sell_date",
                "sell_amount",
                "sell_price_unit",
            ]
            writer = csv.DictWriter(sales_file, fieldnames=fieldnames)
            writer.writeheader()
            print("Sales file created")


def buy_product(product_name=None, amount=None, price_unit=None, expiration_date=None):
    if (
        product_name is None
        or amount is None
        or price_unit is None
        or expiration_date is None
    ):
        return print("Missing one or more arguments.")

    try:
        expire_date = datetime.strptime(expiration_date, "%Y-%m-%d")

        if (expire_date - datetime.today()).days < 0:
            return print("Product expiration date is already reached.")
        elif amount <= 0 or type(amount) is not int:
            return print("Amount needs to be positive and without decimals.")
    except ValueError:
        return print("Expiration date does not exist.")

    else:
        return print("OK")


buy_product("orange", 6, 0.75, "2022-04-28")
