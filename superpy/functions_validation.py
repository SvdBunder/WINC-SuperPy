import csv, os
from datetime import date, datetime
import functions_system

# -----------------------------------------------------------------------------------------
# FUNCTIONS VALIDATION
# -----------------------------------------------------------------------------------------

# Function directly called by the get_method() of Action and Report class and indirectly by
# ImportFromFile class get_method() through the function validate_file_content()
# Checks if given variables / arguments are within parameters and adds all mistakes in a single message.
def validate_arguments(
    product_name=None,
    amount=None,
    price_unit=None,
    expiration_date=None,
    report_date=None,
):
    allowed_products = functions_system.read_products()
    message = []

    # check if product is allowed
    if product_name is not None and product_name.lower() not in allowed_products:
        message.append(
            "Product is not in the list of products approved for sale in this store."
        )

    # check if amount is positive. No decimals allowed is covered in parser type=integer
    if amount is not None and amount <= 0:
        message.append("Amount needs to be a positive number.")

    # check if price is positive and has max 2 decimals
    if price_unit is not None:
        if price_unit <= 0:
            message.append("Price needs to be a positive number.")
        if "." in str(price_unit) and len(str(price_unit).split(".")[-1]) > 2:
            message.append("Price can not have more than 2 decimals.")

    if expiration_date is not None:
        # check if proper format is used
        if len(expiration_date) != 10:
            message.append(
                "Expiration date is not correct. Format needs to be YYYY-MM-DD."
            )
        else:
            try:
                # check if the given date exists
                expire_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()

                # check if the expiration_date has not passed yet => not allowed to buy them.
                if expire_date < date.today():
                    message.append("Expiration date has already passed.")
            except ValueError:
                message.append("Expiration date does not exist.")

    if report_date is not None:
        # check if proper format is used
        if len(report_date) != 10 and len(report_date) != 7 and len(report_date) != 4:
            message.append(
                "Report date is not correct. Format needs to be YYYY-MM-DD, YYYY-MM or YYYY."
            )
        elif len(report_date) != 4:
            # check if the given date exists
            try:
                datetime.strptime(report_date, "%Y-%m-%d")

            except ValueError:

                try:
                    datetime.strptime(report_date, "%Y-%m")

                except ValueError:

                    message.append("Report date does not exist.")

    return message


# Function directly called by the get_method() of ImportFromFile class.
# Checks if the file exists.
def validate_file_existence(file_path, file_name):
    message = []
    file = os.path.join(file_path, file_name)
    if os.path.isfile(file) is False:
        message.append(f"ERROR: file '{file}' does not exist")
    return message


# Function directly called by the get_method() of ImportFromFile class.
# Checks if the content of the file is within parameters by calling validate_arguments for every line.
# Errors are collected in a single message.
def validate_file_content(file_name):
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
                # line count is used in the error message to indicate which lines need to be corrected.
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
