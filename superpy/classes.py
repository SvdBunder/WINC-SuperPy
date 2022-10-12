from datetime import date, datetime
from rich.console import Console
from rich.table import Table
from rich import box
import csv, os, openpyxl
import functions_stock
import functions_validation


class Action:
    def __init__(self, ID, product_name, amount, price_unit, expiration_date):
        self.ID = ID
        self.product_name = product_name
        self.amount = amount
        self.price_unit = price_unit
        self.expiration_date = expiration_date

    def get_method(self, action):
        self.action = action
        method = getattr(self, self.action)
        # validate arguments
        validation = functions_validation.validate_arguments(
            product_name=self.product_name,
            amount=self.amount,
            price_unit=self.price_unit,
            expiration_date=self.expiration_date,
        )
        # if there are errors print error message and exit
        if validation:
            print("\n".join(validation))
            exit(1)

        # if validation is passed call the wanted action (the one stored in args.command)
        else:
            method()
            print("OK")

    def buy(self):

        ID_list = [0]

        with open("purchases.csv", "r+") as purchases_file:
            fieldnames = [
                "ID",
                "product_name",
                "buy_date",
                "buy_amount",
                "buy_price_unit",
                "expiration_date",
            ]

            reader = csv.DictReader(purchases_file, fieldnames=fieldnames)
            writer = csv.DictWriter(purchases_file, fieldnames=fieldnames)

            # To determine which ID number was added last, all ID are added to a list.
            # The new transaction will receive ID number based on the max of the list plus 1.
            for row in reader:
                if row["ID"] != "ID":
                    ID_list.append(int(row["ID"]))

            # save the transaction to the file
            writer.writerow(
                {
                    "ID": max(ID_list) + 1,
                    "product_name": self.product_name.lower(),
                    "buy_date": date.today().strftime("%Y-%m-%d"),
                    "buy_amount": self.amount,
                    "buy_price_unit": self.price_unit,
                    "expiration_date": self.expiration_date,
                }
            )

    def sell(self):
        product_stock = functions_stock.determine_stock(
            product_name=self.product_name, stock_date=date.today()
        )
        # check if there are enough products in stock to sell the wanted amount, if not
        # then print a message and exit.
        amount_in_stock = sum(obj.amount for obj in product_stock)
        if amount_in_stock == 0:
            print("Product is not in stock.")
            exit(1)
        elif amount_in_stock < self.amount:
            print(f"Not enough products in stock: only {amount_in_stock} available.")
            exit(1)

        # if there are enough products:
        else:
            ID_list = [0]
            amount_left = self.amount
            with open("sales.csv", mode="r+") as sales_file:
                fieldnames_sales = [
                    "ID",
                    "buy_ID",
                    "product_name",
                    "sell_date",
                    "sell_amount",
                    "sell_price_unit",
                ]

                reader = csv.DictReader(sales_file, fieldnames=fieldnames_sales)
                writer = csv.DictWriter(sales_file, fieldnames=fieldnames_sales)

                # To determine which ID number was added last, all ID are added to a list.
                # The new transaction will receive ID number based on the max of the list plus 1.
                for line in reader:
                    if line["ID"] != "ID":
                        ID_list.append(int(line["ID"]))

                # First selling the products of purchases that have the oldest expiration_date
                # Then move on to the next purchase till the wanted amount is reached.
                while amount_left > 0:
                    oldest_expiration_date = min(
                        product_stock, key=lambda exp: exp.expiration_date
                    )
                    amount_sold = min(amount_left, oldest_expiration_date.amount)
                    new_ID = max(ID_list) + 1
                    writer.writerow(
                        {
                            "ID": new_ID,
                            "buy_ID": oldest_expiration_date.ID,
                            "product_name": self.product_name.lower(),
                            "sell_date": date.today().strftime("%Y-%m-%d"),
                            "sell_amount": amount_sold,
                            "sell_price_unit": self.price_unit,
                        }
                    )
                    amount_left -= amount_sold
                    ID_list.append(int(new_ID))
                    # removing the purchase with the oldest expiration_date since all is
                    # sold and will not be counted again in the first part of the while loop.
                    product_stock.remove(oldest_expiration_date)


class Report:
    def __init__(self, product_name, report_date, per_product):
        self.product_name = product_name
        self.report_date = report_date
        self.per_product = per_product

    def get_method(self, action):
        # If report inventory is entered with optional argument --per-product then a separate method is called.
        # The inventory_per_product method calls inventory method of every product in stock,
        # creating a table per product.
        self.action = (
            "inventory_per_product"
            if (action == "inventory" and self.per_product)
            else action
        )
        method = getattr(self, self.action)

        # Validate arguments
        validation = functions_validation.validate_arguments(
            product_name=self.product_name,
            report_date=self.report_date,
        )

        # If there are errors print error message and exit
        if validation:
            print("\n".join(validation))
            exit(1)

        # If validation is passed call the wanted action
        else:
            method()

    def revenue(self):
        # report_date is determined by the optional arguments --today, --yesterday and --date
        product_sold = functions_stock.sales(product_name=self.product_name)
        date_intel = functions_stock.date_intel(report_date=self.report_date)
        product_sold_sorted = sorted(product_sold, key=lambda obj: obj.product_name)
        date_length = date_intel["date_length"]
        period = date_intel["message"]
        revenue_per_product = {}

        # Add sales from the alphabetically sorted product_sold if the sale happened on
        # report_date. Date_length determines if is looked at a date, month+year or year.
        for obj in product_sold_sorted:
            if obj.sell_date[0:date_length] == self.report_date:
                revenue_per_product[obj.product_name] = revenue_per_product.get(
                    obj.product_name, 0
                ) + int(obj.amount) * float(obj.price_unit)

        # Calculate revenue of all sales of the requested report_date
        revenue_total = round(sum(revenue_per_product.values()), 2)

        # Use Rich to create a table if optional argument --per-product was used
        console = Console()
        if self.per_product:
            table = Table(
                title=f"Revenue for {period}:",
                title_justify="left",
                title_style="bold",
                show_header=False,
                show_footer=True,
                box=box.HORIZONTALS,
            )

            table.add_column("product name", justify="left", footer="total")
            table.add_column(
                "revenue",
                justify="right",
                footer=f"{'€':<1} {revenue_total:>7.2f}",
            )

            for key, value in revenue_per_product.items():
                table.add_row(key, f"{'€':<1} {round(value,2):>7.2f}")

            return console.print(table)

        # Print a message if --per-product was not used, which one depending on if a product-name was given.
        elif self.product_name is None:
            return print(f"Revenue for {period}: € {revenue_total:.2f}")
        else:
            return print(
                f"Revenue of {self.product_name} for {period}: € {revenue_total:.2f}"
            )

    def profit(self):
        # report_date is determined by the optional arguments --today, --yesterday and --date
        product_sold = functions_stock.sales(product_name=self.product_name)
        product_bought = functions_stock.purchases(product_name=self.product_name)
        product_sold_sorted = sorted(product_sold, key=lambda obj: obj.product_name)
        date_intel = functions_stock.date_intel(report_date=self.report_date)
        date_length = date_intel["date_length"]
        period = date_intel["message"]
        profit_per_product = {}

        # Add sales and purchase transactions that are equal to the requested report_date.
        # Date_length determines if is looked at a date, month+year or year
        for obj_sold in product_sold_sorted:
            if obj_sold.sell_date[0:date_length] == self.report_date:
                profit_per_product[obj_sold.product_name] = profit_per_product.get(
                    obj_sold.product_name, 0
                ) + int(obj_sold.amount) * (
                    float(obj_sold.price_unit)
                    - sum(
                        float(obj_bought.price_unit)
                        for obj_bought in product_bought
                        if obj_sold.buy_ID == obj_bought.ID
                    )
                )

        # Calculate profit of all sales of the requested report_date
        profit_total = round(sum(profit_per_product.values()), 2)

        # Use Rich to create a table if optional argument --per-product was used
        console = Console()
        if self.per_product:
            table = Table(
                title=f"Profit for {period}:",
                title_justify="left",
                title_style="bold",
                show_header=False,
                show_footer=True,
                box=box.HORIZONTALS,
            )

            table.add_column("product name", justify="left", footer="total")
            table.add_column(
                "profit", justify="right", footer=f"{'€':<1} {profit_total:>7.2f}"
            )

            for key, value in profit_per_product.items():
                table.add_row(key, f"{'€':<1} {round(value,2):>7.2f}")

            return console.print(table)

        # Print a message if --per-product was not used, which one depending on if a product-name was given.
        elif self.product_name is None:
            return print(f"Profit for {period}: € {profit_total:.2f}")

        else:
            return print(
                f"Profit of {self.product_name} for {period}: € {profit_total:.2f}"
            )

    def inventory(self):
        # Report_date is determined by the optional arguments --now and --yesterday
        # If a product-name is given then only the data of that product is collected in product_stock
        stock_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        product_stock = functions_stock.determine_stock(
            product_name=self.product_name, stock_date=stock_date.date()
        )

        product_stock_sorted = sorted(product_stock, key=lambda obj: obj.product_name)
        period = stock_date.strftime("%d %B %Y")
        total_amount = sum(int(obj.amount) for obj in product_stock_sorted)
        total_value = sum(
            (int(obj.amount) * float(obj.price_unit)) for obj in product_stock_sorted
        )

        # Use Rich to create a table
        console = Console()

        table = Table(
            title=f"Stock on {period}:",
            title_justify="left",
            title_style="bold",
            show_header=True,
            show_footer=True,
            box=box.SQUARE,
        )

        table.add_column("product name", justify="left", footer="total")
        table.add_column("amount", justify="right", footer=f"{round(total_amount,0)}")
        table.add_column("buy price per unit", justify="right", width=10)
        table.add_column(
            "total value",
            justify="right",
            footer=f"{'€':<1} {round(total_value,2):>10.2f}",
        )
        table.add_column("expiration date", justify="left")

        if product_stock:
            # Add the data from the products in stock
            for obj in product_stock_sorted:
                # Expired products are presented as "expired" instead of the expiration_date
                expiration_date = (
                    obj.expiration_date
                    if datetime.strptime(obj.expiration_date, "%Y-%m-%d")
                    >= datetime.strptime(self.report_date, "%Y-%m-%d")
                    else "expired"
                )
                table.add_row(
                    obj.product_name,
                    f"{obj.amount}",
                    f"{'€':<1} {float(obj.price_unit):>7.2f}",
                    f"{'€':<1} {round(int(obj.amount)*float(obj.price_unit),2):>10.2f}",
                    expiration_date,
                )

            return console.print(table)
        else:
            print("No stock present on requested date.")

    def inventory_per_product(self):
        stock_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        product_stock = functions_stock.determine_stock(stock_date=stock_date.date())
        products_in_stock = []

        if product_stock:
            # Determine which products are in stock
            for obj in product_stock:
                if obj.product_name not in products_in_stock:
                    products_in_stock.append(obj.product_name)

            # Call inventory method for every product in stock
            for product in products_in_stock:
                self.product_name = product
                self.inventory()
        else:
            print("No stock present on requested date.")


class ImportFromFile:
    def __init__(self, file_path, file_name, file_type):
        self.file_path = file_path
        self.file_name = file_name
        self.file_type = file_type

    def get_method(self, action):
        self.action = action
        method = getattr(self, self.action)

        # Check if the file exists
        validate_existence = functions_validation.validate_file_existence(
            file_path=self.file_path, file_name=self.file_name
        )
        # If not then print a message and exit
        if validate_existence:
            print(validate_existence)
            exit(1)
        else:
            self.file = os.path.join(self.file_path, self.file_name)

            # Create a temp.csv file using a method based on the file_type
            convert_method = getattr(self, self.file_type + "_to_temp_csv")
            convert_method()

            # Validate the content of the file and execute import method if validation is passed
            validation = functions_validation.validate_file_content(
                file_name="temp.csv"
            )
            if validation:
                print("\n".join(validation))
                exit(1)
            else:
                method()

    def csv_to_temp_csv(self):
        transaction = self.action.removeprefix("import_")

        with open("temp.csv", mode="w") as write_file:
            fieldnames_buy = [
                "product_name",
                "amount",
                "price_unit",
                "expiration_date",
            ]
            fieldnames_sell = ["product_name", "amount", "price_unit"]
            fieldnames = fieldnames_buy if transaction == "buy" else fieldnames_sell
            writer = csv.DictWriter(write_file, fieldnames=fieldnames)
            writer.writeheader()

            # Since csv files standard delimiter is based on regional settings the
            # csv.Sniffer is used to detect which one is used.
            with open(self.file, newline="") as read_file:
                dialect = csv.Sniffer().sniff(read_file.read(1024))
                read_file.seek(0)

                reader = csv.DictReader(read_file, dialect=dialect)

                # writing data to a temporary csv file
                for line in reader:
                    if transaction == "buy":
                        writer.writerow(
                            {
                                "product_name": line["product_name"],
                                "amount": line["amount"],
                                "price_unit": line["price_unit"],
                                "expiration_date": line["expiration_date"],
                            }
                        )

                    else:
                        writer.writerow(
                            {
                                "product_name": line["product_name"],
                                "amount": line["amount"],
                                "price_unit": line["price_unit"],
                            }
                        )

    def xlsx_to_temp_csv(self):
        xlsx_obj = openpyxl.load_workbook(self.file).active

        m_row = xlsx_obj.max_row
        m_col = xlsx_obj.max_column
        headers = {}
        transaction = self.action.removeprefix("import_")

        # determining which column contains what header
        for col in range(1, m_col + 1):
            cell_obj = xlsx_obj.cell(row=1, column=col)
            headers[cell_obj.value] = col

        # writing data to a temporary csv file
        with open("temp.csv", mode="w") as write_file:
            fieldnames_buy = ["product_name", "amount", "price_unit", "expiration_date"]
            fieldnames_sell = ["product_name", "amount", "price_unit"]
            fieldnames = fieldnames_buy if transaction == "buy" else fieldnames_sell
            writer = csv.DictWriter(write_file, fieldnames=fieldnames)
            writer.writeheader()

            for line in range(2, m_row + 1):
                product_name_obj = xlsx_obj.cell(
                    row=line, column=headers["product_name"]
                )
                amount_obj = xlsx_obj.cell(row=line, column=headers["amount"])
                price_unit_obj = xlsx_obj.cell(row=line, column=headers["price_unit"])

                if transaction == "buy":
                    expiration_date_obj = xlsx_obj.cell(
                        row=line, column=headers["expiration_date"]
                    )
                    writer.writerow(
                        {
                            "product_name": product_name_obj.value,
                            "amount": amount_obj.value,
                            "price_unit": price_unit_obj.value,
                            "expiration_date": expiration_date_obj.value,
                        }
                    )

                else:
                    writer.writerow(
                        {
                            "product_name": product_name_obj.value,
                            "amount": amount_obj.value,
                            "price_unit": price_unit_obj.value,
                        }
                    )

    def import_buy(self):
        # For every line in temp.csv an Action classobject is made and the buy method is called.
        line_count = 0
        with open("temp.csv") as read_file:
            fieldnames = ["product_name", "amount", "price_unit", "expiration_date"]
            reader = csv.DictReader(read_file, fieldnames=fieldnames)

            for line in reader:
                if line["product_name"] != "product_name":
                    line_count += 1
                    obj = Action(
                        ID=None,
                        product_name=line["product_name"],
                        price_unit=float(line["price_unit"]),
                        amount=int(line["amount"]),
                        expiration_date=line["expiration_date"],
                    )
                    obj.buy()

        # temp.csv is deleted and number of successfully imported transactions is printed.
        os.remove("temp.csv")
        return print(f"Import completed: {line_count} purchases transactions imported.")

    def import_sell(self):
        # For every line in temp.csv an Action classobject is made and the sell method is called.
        line_count = 0
        with open("temp.csv") as read_file:
            fieldnames = ["product_name", "amount", "price_unit"]
            reader = csv.DictReader(read_file, fieldnames=fieldnames)

            for line in reader:
                if line["product_name"] != "product_name":
                    line_count += 1
                    obj = Action(
                        ID=None,
                        product_name=line["product_name"],
                        price_unit=float(line["price_unit"]),
                        amount=int(line["amount"]),
                        expiration_date=None,
                    )
                    obj.sell()

        # temp.csv is deleted and number of successfully imported transactions is printed.
        os.remove("temp.csv")
        return print(f"Import completed: {line_count} sales transactions imported.")
