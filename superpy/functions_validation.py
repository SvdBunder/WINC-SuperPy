import csv
from datetime import date, datetime
import functions_system as SPFsystem

# -----------------------------------------------------------------------------------------
# FUNCTIONS VALIDATION
# -----------------------------------------------------------------------------------------
#


def validate_arguments(
    product_name=None,
    amount=None,
    price_unit=None,
    expiration_date=None,
    report_date=None,
):
    allowed_products = SPFsystem.read_products()
    message = []

    if product_name is not None and product_name.lower() not in allowed_products:
        message.append(
            "Product is not in the list of products approved for sale in this store."
        )

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

    if report_date is not None:
        if len(report_date) != 10 and len(report_date) != 7 and len(report_date) != 4:
            message.append(
                "Report date is not correct. Format needs to be YYYY-MM-DD, YYYY-MM or YYYY."
            )
        elif len(report_date) != 4:
            try:
                datetime.strptime(report_date, "%Y-%m-%d")

            except ValueError:

                try:
                    datetime.strptime(report_date, "%Y-%m")

                except ValueError:

                    message.append("Report date does not exist.")

    return message


def validate_file(file_name):
    message = []
    line_count = 0

    with open(file_name) as read_file:
        fieldnames = [
            "product_name",
            "amount",
            "price_unit",
            "expiration_date",
        ]
        reader = csv.DictReader(read_file, fieldnames=fieldnames)

        for line in reader:
            if line["product_name"] != "product_name":
                line_count += 1
                validation = validate_arguments(
                    product_name=line["product_name"],
                    amount=int(line["amount"]),
                    price_unit=float(line["price_unit"]),
                    expiration_date=line["expiration_date"],
                    report_date=None,
                )

                if validation:
                    message.append(
                        f"Errors in line {line_count} of the file: {validation}"
                    )

    return message