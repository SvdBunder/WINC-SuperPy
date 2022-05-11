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


def buy_product(
    product_name=None,
    buy_date=date.today().strftime("%Y-%m-%d"),
    amount=None,
    price_unit=None,
    expiration_date=None,
):
    # check if input is complete and correct
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
        elif price_unit <= 0 or (
            "." in str(price_unit) and len(str(price_unit).split(".")[-1]) > 2
        ):
            return print(
                "Price per unit needs to be positive and can not have more than 2 decimals."
            )
    except ValueError:
        return print("Expiration date does not exist.")
    # determining the last ID-number registered in the csv file
    else:
        ID_list = [0]
        with open("purchases.csv", "r") as read_file:
            fieldnames = [
                "ID",
                "product_name",
                "buy_date",
                "buy_amount",
                "buy_price_unit",
                "expiration_date",
            ]

            reader = csv.DictReader(read_file, fieldnames=fieldnames)

            for row in reader:
                if row["ID"] != "ID":
                    ID_list.append(int(row["ID"]))
        # add the purchase to the csv file
        with open("purchases.csv", "a") as append_file:
            fieldnames = [
                "ID",
                "product_name",
                "buy_date",
                "buy_amount",
                "buy_price_unit",
                "expiration_date",
            ]
            writer = csv.DictWriter(append_file, fieldnames=fieldnames)

            writer.writerow(
                {
                    "ID": max(ID_list) + 1,
                    "product_name": product_name.lower(),
                    "buy_date": buy_date,
                    "buy_amount": amount,
                    "buy_price_unit": price_unit,
                    "expiration_date": expiration_date,
                }
            )

        return print("OK")


def sell_product(product_name=None, amount=None, price_unit=None):
    # check if input is complete and correct
    if product_name is None or amount is None or price_unit is None:
        return print("Missing one or more arguments.")
    elif amount <= 0 or type(amount) is not int:
        return print("Amount needs to be positive and without decimals.")
    elif price_unit <= 0 or (
        "." in str(price_unit) and len(str(price_unit).split(".")[-1]) > 2
    ):
        return print(
            "Price per unit needs to be positive and can not have more than 2 decimals."
        )
    # add purchases to dictionary and determine amount in stock
    else:
        product_stock = {}
        with open("purchases.csv", "r") as read_purchases:
            fieldnames_purchase = [
                "ID",
                "product_name",
                "buy_date",
                "buy_amount",
                "buy_price_unit",
                "expiration_date",
            ]

            purchase_reader = csv.DictReader(
                read_purchases, fieldnames=fieldnames_purchase
            )

            for row in purchase_reader:
                if row["product_name"] == product_name.lower():

                    product_stock[int(row["ID"])] = int(row["buy_amount"])

        with open("sales.csv", "r") as read_sales:
            fieldnames_sales = [
                "ID",
                "buy_ID",
                "product_name",
                "sell_date",
                "sell_amount",
                "sell_price_unit",
            ]

            sales_reader = csv.DictReader(read_sales, fieldnames=fieldnames_sales)

            for row in sales_reader:
                if row["product_name"] == product_name.lower():
                    product_stock[int(row["buy_ID"])] = product_stock[
                        int("buy_ID")
                    ] - int(row["sell_amount"])

        amount_in_stock = sum(product_stock.values())
        if amount_in_stock == 0:
            return print("Product is not in stock.")
        elif amount_in_stock < amount:
            return print(
                f"Not enough products in stock. Only {amount_in_stock} are available."
            )
        else:

            return print(min(product_stock.keys()))


sell_product(product_name="orange", amount=1, price_unit=0.80)
sell_product(product_name="Orange", amount=31, price_unit=0.80)
sell_product(product_name="grape", amount=1, price_unit=0.80)
