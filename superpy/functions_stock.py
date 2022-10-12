import csv
from datetime import datetime, date
from types import SimpleNamespace
import functions_system

# -----------------------------------------------------------------------------------------
# FUNCTIONS CALLED BY SUPERPY CLASSES
# -----------------------------------------------------------------------------------------

# Function used in Report class
# Generates a dictionary based on argument report_date with a "date_length" and "message" =
# description of the report_date. Date_length is used to slice the buy and sell date to match
# the format of the report_date: when report_date is a year plus a month then the class method
# needs to look at the first 7 positions of a buy or sell date to determine if it can be
# negated or added.
def date_intel(report_date):
    # report date is a day, format YYYY-MM-DD
    if len(report_date) == 10:
        date_length = 10
        if (
            datetime.strptime(report_date, "%Y-%m-%d").date()
            == functions_system.read_time()
        ):
            message = "today so far"
        elif datetime.strptime(
            report_date, "%Y-%m-%d"
        ).date() == functions_system.read_time(-1):
            message = "yesterday"
        else:
            message = datetime.strptime(report_date, "%Y-%m-%d").strftime("%d %B %Y")

    # report date is a month, format YYYY-MM
    elif len(report_date) == 7:
        date_length = 7
        message = datetime.strptime(report_date, "%Y-%m").strftime("%B %Y")

    # report date is a year, format YYYY
    else:
        date_length = 4
        message = report_date

    outcome = {"date_length": date_length, "message": message}
    return outcome


# Function used in (1) determine_stock(); (2) Report class - methods revenue and profit
# Generates a list of all stored sales and turns every sale in a SimpleNamespace classobject.
# Using SimpleNamespace instead of Action class to (1) prevent import loop; (2) not wanting
# to add attributes to the class that are not entered as a CLI argument; (3) not wanting to
# use **kwargs in the class just to be free to add attributes without making them mandatory
# for every object of that class.
def sales(product_name=None):
    product_sold = []

    with open("sales.csv", mode="r") as sales_file:
        fieldnames_sales = [
            "ID",
            "buy_ID",
            "product_name",
            "sell_date",
            "sell_amount",
            "sell_price_unit",
        ]

        sales_reader = csv.DictReader(sales_file, fieldnames=fieldnames_sales)

        # skip the header
        next(sales_reader)

        if product_name is not None:
            # only add the transactions of the specified product_name
            for line in sales_reader:
                if line["product_name"] == product_name.lower():
                    product_sold.append(
                        SimpleNamespace(
                            ID=line["ID"],
                            buy_ID=line["buy_ID"],
                            product_name=line["product_name"],
                            amount=line["sell_amount"],
                            sell_date=line["sell_date"],
                            price_unit=line["sell_price_unit"],
                        )
                    )
        else:
            # add all transactions if no product_name is given
            for line in sales_reader:
                product_sold.append(
                    SimpleNamespace(
                        ID=line["ID"],
                        buy_ID=line["buy_ID"],
                        product_name=line["product_name"],
                        amount=line["sell_amount"],
                        sell_date=line["sell_date"],
                        price_unit=line["sell_price_unit"],
                    )
                )
        return product_sold


# Function used in (1) determine_stock(); (2) Report class - method profit
# Generates a list of all stored purchases and turns every purchase in a SimpleNamespace classobject.
def purchases(product_name=None):
    product_bought = []

    with open("purchases.csv", mode="r") as purchases_file:
        fieldnames_purchases = [
            "ID",
            "product_name",
            "buy_date",
            "buy_amount",
            "buy_price_unit",
            "expiration_date",
        ]

        purchases_reader = csv.DictReader(
            purchases_file, fieldnames=fieldnames_purchases
        )

        # skip the header
        next(purchases_reader)

        if product_name is not None:
            # only add the transactions of the specified product_name
            for line in purchases_reader:
                if line["product_name"] == product_name.lower():
                    product_bought.append(
                        SimpleNamespace(
                            ID=line["ID"],
                            product_name=line["product_name"],
                            buy_date=line["buy_date"],
                            amount=line["buy_amount"],
                            price_unit=line["buy_price_unit"],
                            expiration_date=line["expiration_date"],
                        )
                    )
        else:
            # add all transactions if no product_name is given
            for line in purchases_reader:
                product_bought.append(
                    SimpleNamespace(
                        ID=line["ID"],
                        product_name=line["product_name"],
                        buy_date=line["buy_date"],
                        amount=line["buy_amount"],
                        price_unit=line["buy_price_unit"],
                        expiration_date=line["expiration_date"],
                    )
                )
        return product_bought


# Function used in (1) functions_system.manage_products(); (2) Report class - method inventory
# (3) Action class - method sell.
# Generates products in stock based on sales(), purchases()
def determine_stock(product_name=None, stock_date=date.today()):
    product_stock = []
    product_sold = sales(product_name)
    product_bought = purchases(product_name)

    for obj_bought in product_bought:
        # Only add purchases that are bought on a date before stock_date
        if datetime.strptime(obj_bought.buy_date, "%Y-%m-%d").date() <= stock_date:
            # Determine if everything is sold or not
            amount_left = int(obj_bought.amount) - sum(
                int(obj_sold.amount)
                for obj_sold in product_sold
                # Only takes in account sales that happened before stock_date
                if (
                    obj_sold.buy_ID == obj_bought.ID
                    and datetime.strptime(obj_sold.sell_date, "%Y-%m-%d").date()
                    <= stock_date
                )
            )

            # If not everything is sold then add to the product_stock list as a SimpleNamespace
            # classobject
            if amount_left > 0:
                product_stock.append(
                    SimpleNamespace(
                        ID=obj_bought.ID,
                        product_name=obj_bought.product_name,
                        amount=amount_left,
                        price_unit=float(obj_bought.price_unit),
                        expiration_date=obj_bought.expiration_date,
                    )
                )

    return product_stock
