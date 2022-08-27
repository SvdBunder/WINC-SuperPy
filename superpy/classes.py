from datetime import date, datetime
import csv
import functions as SPfunctions


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
        method()

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

            for row in reader:
                if row["ID"] != "ID":  # zodat de header niet wordt meegenomen
                    ID_list.append(int(row["ID"]))

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

        return print("OK")

    def sell(self):
        product_stock = SPfunctions.determine_stock(product_name=self.product_name)
        amount_in_stock = sum(obj.amount for obj in product_stock)
        if amount_in_stock == 0:
            print("Product is not in stock.")
            exit(1)
        elif amount_in_stock < self.amount:
            print(f"Not enough products in stock: only {amount_in_stock} available.")
            exit(1)
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

                for line in reader:
                    if line["ID"] != "ID":
                        ID_list.append(int(line["ID"]))

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
                    product_stock.remove(oldest_expiration_date)

            return print("OK")


class Report:
    def __init__(self, product_name, report_date, per_product):
        self.product_name = product_name
        self.report_date = report_date
        self.per_product = per_product

    def get_method(self, action):
        self.action = action
        method = getattr(self, self.action)
        method()

    def revenue(self):
        product_sold = SPfunctions.sales(product_name=self.product_name)
        date_intel = SPfunctions.date_intel(report_date=self.report_date)
        date_length = date_intel["date_length"]
        period = date_intel["message"]
        revenue = 0
        revenue_per_product = {}
        revenue_list = []

        if self.per_product:
            for obj in product_sold:
                if obj.sell_date[0:date_length] == self.report_date:
                    if obj.product_name in revenue_per_product.keys():
                        revenue_per_product[obj.product_name] = revenue_per_product.get(
                            obj.product_name
                        ) + int(obj.amount) * float(obj.price_unit)
                    else:
                        revenue_per_product[obj.product_name] = int(obj.amount) * float(
                            obj.price_unit
                        )

            for key, value in revenue_per_product.items():
                revenue_list.append(f"      {key}        € {round(value,2):.2f}")
            return (
                print(f"Revenue for {period}:"),
                print("\n".join(revenue_list)),
                print(
                    f"      total        € {round(sum(revenue_per_product.values()),2):.2f}"
                ),
            )

        else:
            for obj in product_sold:
                if obj.sell_date[0:date_length] == self.report_date:

                    revenue += int(obj.amount) * float(obj.price_unit)

            return (
                print(f"Revenue for {period}: € {round(revenue, 2):.2f}")
                if self.product_name is None
                else print(
                    f"Revenue of {self.product_name} for {period}: € {round(revenue, 2):.2f}"
                )
            )

    def profit(self):
        product_sold = SPfunctions.sales(product_name=self.product_name)
        product_bought = SPfunctions.purchases(product_name=self.product_name)
        date_intel = SPfunctions.date_intel(report_date=self.report_date)
        date_length = date_intel["date_length"]
        period = date_intel["message"]
        profit = 0
        profit_per_product = {}
        profit_list = []

        if self.per_product:
            for obj_sold in product_sold:
                if obj_sold.sell_date[0:date_length] == self.report_date:
                    if obj_sold.product_name in profit_per_product.keys():
                        profit_per_product[
                            obj_sold.product_name
                        ] = profit_per_product.get(obj_sold.product_name) + int(
                            obj_sold.amount
                        ) * (
                            float(obj_sold.price_unit)
                            - sum(
                                float(obj_bought.price_unit)
                                for obj_bought in product_bought
                                if obj_sold.buy_ID == obj_bought.ID
                            )
                        )

                    else:
                        profit_per_product[obj_sold.product_name] = int(
                            obj_sold.amount
                        ) * (
                            float(obj_sold.price_unit)
                            - sum(
                                float(obj_bought.price_unit)
                                for obj_bought in product_bought
                                if obj_sold.buy_ID == obj_bought.ID
                            )
                        )

            for key, value in profit_per_product.items():
                profit_list.append(f"      {key}        € {round(value,2):.2f}")

            return (
                print(f"Profit for {period}:"),
                print("\n".join(profit_list)),
                print(
                    f"      total        € {round(sum(profit_per_product.values()),2):.2f}"
                ),
            )

        else:
            for obj_sold in product_sold:
                if obj_sold.sell_date[0:date_length] == self.report_date:

                    profit += int(obj_sold.amount) * (
                        float(obj_sold.price_unit)
                        - sum(
                            float(obj_bought.price_unit)
                            for obj_bought in product_bought
                            if obj_sold.buy_ID == obj_bought.ID
                        )
                    )

            return (
                print(f"Profit for {period}: € {round(profit, 2):.2f}")
                if self.product_name is None
                else print(
                    f"Profit of {self.product_name} for {period}: € {round(profit, 2):.2f}"
                )
            )

    def inventory(self):
        product_stock = SPfunctions.determine_stock(product_name=self.product_name)
        date_intel = SPfunctions.date_intel(report_date=self.report_date)
        period = date_intel["message"]
        stock_list = []
        total_amount = 0
        total_value = 0
        for obj in product_stock:
            stock_list.append(
                f"{obj.product_name} | {obj.amount} | € {float(obj.price_unit):.2f} | € {round(int(obj.amount) * float(obj.price_unit),2):.2f} | {obj.expiration_date}"
            )
            total_amount += int(obj.amount)
            total_value += round(int(obj.amount) * float(obj.price_unit), 2)

        return (
            print(
                f"Inventory on {period}: \nProduct Name | Amount | Buy Price Per Unit | Total Value | Expiration Date"
            ),
            print("\n".join(stock_list)),
            print(
                f"GRAND TOTAL                    {total_amount}                  € {total_value:.2f}"
            ),
        )
