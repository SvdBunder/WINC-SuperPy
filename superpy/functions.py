import csv, os.path
from datetime import date, datetime, timedelta
from types import SimpleNamespace

# -----------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------
#
def report_time(days=0):

    with open("SuperPyDate.txt", "r") as reader:
        saved_text = reader.read()
        saved_date = datetime.strptime(saved_text, "%Y-%m-%d").date()
        report_date = saved_date + timedelta(days)
        return report_date


def save_time(days=0, restore=False):
    new_date = date.today() + timedelta(days)

    if os.path.isfile("SuperPyDate.txt") is False:
        with open("SuperPyDate.txt", "w") as file:
            file.write(new_date.strftime("%Y-%m-%d"))
    else:

        saved_date = report_time()

        if saved_date == new_date:
            return

        elif saved_date > new_date and restore is False:
            return print(
                f"Registered date is {saved_date} and exceeds current date. \nIf this is not the correct date please execute the --restore-time command."
            )

        else:

            with open("SuperPyDate.txt", "w") as writer:

                writer.write(new_date.strftime("%Y-%m-%d"))

                return print("OK")


def date_intel(report_date):
    if len(report_date) == 10:
        date_length = 10
        if datetime.strptime(report_date, "%Y-%m-%d").date() == report_time():
            message = "today so far"
        elif datetime.strptime(report_date, "%Y-%m-%d").date() == report_time(-1):
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


def check_files():
    if os.path.isfile("purchases.csv") is False:

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

    if os.path.isfile("sales.csv") is False:

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


def validate_arguments(amount, price_unit, expiration_date, manual_report_date):

    message = []
    if amount is not None and amount <= 0:

        message.append("Amount needs to be a positive number.")

    if price_unit is not None:
        if price_unit <= 0:
            message.append("Price needs to be a positive number.")
        if "." in str(price_unit) and len(str(price_unit).split(".")[-1]) > 2:
            message.append("Price can not have more than 2 decimals.")
    if expiration_date is not None:
        if len(expiration_date) != 10:
            message.append(
                "Expiration date is not correct. Format needs to be YYYY-MM-DD."
            )
        else:
            try:
                expire_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()

                if expire_date < date.today():
                    message.append("Expiration date is already reached.")
            except ValueError:
                message.append("Expiration date does not exist.")

    if manual_report_date is not None:
        if (
            len(manual_report_date) != 10
            and len(manual_report_date) != 7
            and len(manual_report_date) != 4
        ):
            message.append(
                "Report date is not correct. Format needs to be YYYY-MM-DD, YYYY-MM or YYYY."
            )
        elif len(manual_report_date) != 4:
            try:
                datetime.strptime(manual_report_date, "%Y-%m-%d")

            except ValueError:

                try:
                    datetime.strptime(manual_report_date, "%Y-%m")

                except ValueError:

                    message.append("Report date does not exist.")

    return message


def sales(product_name=None):
    product_sold = []

    with open("sales.csv", "r") as sales_file:
        fieldnames_sales = [
            "ID",
            "buy_ID",
            "product_name",
            "sell_date",
            "sell_amount",
            "sell_price_unit",
        ]

        sales_reader = csv.DictReader(sales_file, fieldnames=fieldnames_sales)

        if product_name is not None:
            for line in sales_reader:
                if line["ID"] != "ID" and line["product_name"] == product_name.lower():
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
                if line["ID"] != "ID":
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
    with open("purchases.csv", "r") as purchases_file:
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

        if product_name is not None:
            for line in purchases_reader:
                if line["ID"] != "ID" and line["product_name"] == product_name.lower():
                    product_bought.append(
                        SimpleNamespace(
                            ID=line["ID"],
                            product_name=line["product_name"],
                            amount=line["buy_amount"],
                            price_unit=line["buy_price_unit"],
                            expiration_date=line["expiration_date"],
                        )
                    )
        else:
            for line in purchases_reader:
                if line["ID"] != "ID":
                    product_bought.append(
                        SimpleNamespace(
                            ID=line["ID"],
                            product_name=line["product_name"],
                            amount=line["buy_amount"],
                            price_unit=line["buy_price_unit"],
                            expiration_date=line["expiration_date"],
                        )
                    )
        return product_bought


def determine_stock(product_name=None):
    product_stock = []
    product_sold = sales(product_name)
    product_bought = purchases(product_name)

    for obj_bought in product_bought:
        amount_left = int(obj_bought.amount) - sum(
            int(obj_sold.amount)
            for obj_sold in product_sold
            if obj_sold.buy_ID == obj_bought.ID
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
