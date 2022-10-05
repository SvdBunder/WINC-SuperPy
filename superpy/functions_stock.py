import csv
from datetime import datetime, date
from types import SimpleNamespace
import functions_system as SPfunctions

# -----------------------------------------------------------------------------------------
# FUNCTIONS CALLED BY SUPERPY CLASSES
# -----------------------------------------------------------------------------------------
#
def date_intel(report_date):

    if len(report_date) == 10:
        date_length = 10
        if datetime.strptime(report_date, "%Y-%m-%d").date() == SPfunctions.read_time():
            message = "today so far"
        elif datetime.strptime(report_date, "%Y-%m-%d").date() == SPfunctions.read_time(
            -1
        ):
            message = "yesterday"
        else:
            message = datetime.strptime(report_date, "%Y-%m-%d").strftime("%d %B %Y")

    elif len(report_date) == 7:
        date_length = 7
        message = datetime.strptime(report_date, "%Y-%m").strftime("%B %Y")
    else:
        date_length = 4
        message = report_date

    outcome = {"date_length": date_length, "message": message}
    return outcome


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
        next(sales_reader)
        if product_name is not None:
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

        next(purchases_reader)

        if product_name is not None:
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


def determine_stock(product_name=None, stock_date=date.today()):
    product_stock = []
    product_sold = sales(product_name)
    product_bought = purchases(product_name)

    for obj_bought in product_bought:
        if obj_bought.buy_date <= stock_date:
            amount_left = int(obj_bought.amount) - sum(
                int(obj_sold.amount)
                for obj_sold in product_sold
                if (
                    obj_sold.buy_ID == obj_bought.ID
                    and obj_sold.sell_date <= stock_date
                )
            )

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
