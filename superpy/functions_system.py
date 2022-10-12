import csv, os
from datetime import date, datetime, timedelta


# -----------------------------------------------------------------------------------------
# FUNCTIONS SYSTEM MAINTENANCE
# -----------------------------------------------------------------------------------------

# Function used in (1) save_time(); (2) CLI_parser - level2_report_inventory_parser - optional
# arguments --now and --yesterday; (3) CLI_router - optional argument --report-time
# Reads the stored systemtime and returns system date plus the entered amount of days.
def read_time(days=0):

    with open("systemtime.txt", "r") as reader:
        saved_text = reader.read()
        saved_date = datetime.strptime(saved_text, "%Y-%m-%d").date()
        report_date = saved_date + timedelta(days)
        return report_date


# Function used in (1) superpy; (2) CLI_router - optional arguments --advance-time and --restore-time.
# Stores the systemtime that superpy sees as "today" in a txt file.
def save_time(days=0, restore=False):
    new_date = date.today() + timedelta(days)

    if os.path.isfile("systemtime.txt") is False:
        with open("systemtime.txt", "w") as file:
            file.write(new_date.strftime("%Y-%m-%d"))

    else:
        saved_date = read_time()

        # to prevent that the advanced time is replaced by date today by calling the function in superpy
        # date is only saved if it is later in time than the stored systemtime unless --restore-time is used.
        if saved_date < new_date or restore:
            with open("systemtime.txt", "w") as writer:

                writer.write(new_date.strftime("%Y-%m-%d"))

        if restore or days != 0:
            return print("OK")


# Function used in superpy to create all files that are needed to store product, purchase
# and sales data.
def create_files():
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

    if os.path.isfile("products.csv") is False:
        with open("products.csv", mode="w") as products_file:

            writer = csv.DictWriter(products_file, fieldnames=["product_name"])
            writer.writeheader()


# Function used in (1) manage_products(); (2) functions_validation.validate_arguments() to check if a product
# is allowed.
def read_products():
    product_list = []

    with open("products.csv", mode="r") as read_file:
        reader = csv.DictReader(read_file, fieldnames=["product_name"])
        for line in reader:
            if line["product_name"] != "product_name":
                product_list.append(line["product_name"])

    return product_list


# Function used in CLI_router - optional arguments --product-list, --add-product and
# --delete-product to report, add or delete products in the stored product list.
# All product-names are always looked at and stored in lowercase, due to python being case sensitive
# and seeing a word with capital as a different item than a word without capital.
def manage_products(product_list=False, add_product=None, delete_product=None):
    # Importing only the wanted function and not the entire module at the start of the file
    # to prevent an import error => both modules want to import each other.
    from functions_stock import determine_stock

    message = []
    allowed_products = []
    saved_products = read_products()
    products_to_be_added = add_product
    products_to_be_deleted = delete_product

    # Storing the currently allowed products in a list for manipulation by add or delete.
    # Save_products is not changed => used to determine how many products are added or deleted,
    # taking into account that some of the given products already exist or can not be deleted.
    for item_saved in saved_products:
        allowed_products.append(item_saved)

    # Only activates this part for optional argument --product-list; printing a list of allowed products.
    if product_list:
        if bool(saved_products) is False:
            return print(
                "Allowed product list is empty. Please add products using the --add-product command."
            )
        else:
            return (print("Allowed products:"), print("\n".join(saved_products)))

    # Only activates this part for optional argument --delete-product
    # Multiple products can be deleted at one time
    elif delete_product is not None:

        for item in products_to_be_deleted:
            item_del = item.lower()
            product_stock = determine_stock(item_del)
            amount_in_stock = sum(obj.amount for obj in product_stock)

            # Check if there is anything to be deleted
            if item_del not in allowed_products:
                message.append(
                    f"Product {item_del} is not in the list of products approved for sale in this store."
                )
            # Check if there is any in stock => if there is the product can not be deleted or you can not sell it anymore.
            elif int(amount_in_stock) > 0:
                message.append(
                    f"Product {item_del} will not be deleted: there still are {amount_in_stock} units in stock."
                )

            else:
                # product is deleted
                allowed_products.remove(item_del)
        message.append(
            f"{len(saved_products)-len(allowed_products)} products are deleted."
        )

    # Only activates this part for optional argument --add-product
    # Multiple products can be added at one time
    elif add_product is not None:
        for item in products_to_be_added:
            item_add = item.lower()
            # Check if the product does not exist yet before adding it.
            if item_add in allowed_products:
                message.append(f"Product {item_add} already exists.")
            else:
                allowed_products.append(item_add)
        message.append(
            f"{len(allowed_products)-len(saved_products)} products are added."
        )

    # Storing the new allowed products list, truncating the products.csv file.
    with open("products.csv", mode="w") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=["product_name"])
        writer.writeheader()
        for product in allowed_products:

            writer.writerow({"product_name": product})

    return print("\n".join(message))
