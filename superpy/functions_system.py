import csv, os
from datetime import date, datetime, timedelta


# -----------------------------------------------------------------------------------------
# FUNCTIONS SYSTEM MAINTENANCE
# -----------------------------------------------------------------------------------------
#
def read_time(days=0):

    with open("systemtime.txt", "r") as reader:
        saved_text = reader.read()
        saved_date = datetime.strptime(saved_text, "%Y-%m-%d").date()
        report_date = saved_date + timedelta(days)
        return report_date


def save_time(days=0, restore=False):
    new_date = date.today() + timedelta(days)

    if os.path.isfile("systemtime.txt") is False:
        with open("systemtime.txt", "w") as file:
            file.write(new_date.strftime("%Y-%m-%d"))

    else:
        saved_date = read_time()

        if saved_date < new_date or restore:
            with open("systemtime.txt", "w") as writer:

                writer.write(new_date.strftime("%Y-%m-%d"))

            if restore or days != 0:
                return print("OK")


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


def read_products():
    product_list = []

    with open("products.csv", mode="r") as read_file:
        reader = csv.DictReader(read_file, fieldnames=["product_name"])
        for line in reader:
            if line["product_name"] != "product_name":
                product_list.append(line["product_name"])

    return product_list


def manage_products(product_list=False, add_product=None, delete_product=None):
    from functions_stock import determine_stock

    message = []
    allowed_products = []
    saved_products = read_products()
    products_to_be_added = add_product
    products_to_be_deleted = delete_product

    for item_saved in saved_products:
        allowed_products.append(item_saved)

    if product_list:
        if bool(saved_products) is False:
            return print(
                "Allowed product list is empty. Please add products using the --add-product command."
            )
        else:
            return (print("Allowed products:"), print("\n".join(saved_products)))

    elif delete_product is not None:

        for item in products_to_be_deleted:
            item_del = item.lower()
            product_stock = determine_stock(item_del)
            amount_in_stock = sum(obj.amount for obj in product_stock)
            if item_del not in allowed_products:
                message.append(
                    f"Product {item_del} is not in the list of products approved for sale in this store."
                )

            elif int(amount_in_stock) > 0:
                message.append(
                    f"Product {item_del} will not be deleted: there still are {amount_in_stock} units in stock."
                )

            else:

                allowed_products.remove(item_del)
        message.append(
            f"{len(saved_products)-len(allowed_products)} products are deleted."
        )

    elif add_product is not None:
        for item in products_to_be_added:
            item_add = item.lower()
            if item_add in allowed_products:
                message.append(f"Product {item_add} already exists.")
            else:
                allowed_products.append(item_add)
        message.append(
            f"{len(allowed_products)-len(saved_products)} products are added."
        )

    with open("products.csv", mode="w") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=["product_name"])
        writer.writeheader()
        for product in allowed_products:

            writer.writerow({"product_name": product})

    return print("\n".join(message))
