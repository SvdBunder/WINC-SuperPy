# SUPERPY USAGE GUIDE
---

## 1. General information

The program is written in python and uses Argparse for the command line interface (CLI).
It contains the following python files:
- SuperPy: main file initiating the program.
- CLI_router: determines which action needs to be executed based on CLI input.
*Imported in: SuperPy*
- CLI_parser: creating the CLI-tool.
*Imported in: CLI_router.*
- classes: several sections of the program with similar arguments are wrapped in classes.
*Imported in: CLI_router.*
- functions_stock: functions to collect the saved sales and purchases data and determine stock.
*Imported in: classes, functions_system (only in the function "manage_products").*
- functions_system: functions for system maintenance such as system time and allowed products.
*Imported in: SuperPy, CLI_router, CLI_parser, functions_validation, functions_stock.*
- functions_validation: functions to validate the CLI input.
*Imported in: classes.*

The purpose of this guide is to describe how the program operates, demonstrating it by supplying examples and their results.
For demonstration purposes the GitHub repository includes 4 test import files (2 for sales and 2 for purchases, each has a faulty and a correct file) next to this guide, a readme.md and the aforementioned python files. *Only use these test files **BEFORE** the program has the go-live and delete the created sales and purchases CSV-files from the superpy-directory when done testing.*

## 2. Program operation

### 2.1. Getting started
CLI input:

```
>>> python superpy.py
```

This triggers 3 actions:
1. functions_system.create_file(): creates the CSV files for sales, purchases and products if they does not exist yet. This function is triggered by every CLI command given.
2. functions_system.save_time(): creates a txt file for saving system time ("systemtime.txt") if the file does not exist and saves today's date (format: YYYY-MM-DD) if the date in the txt file predates today. The saved systemtime is used for reports only and assures that they are based on recent figures. This function is triggered by every CLI command given.
3. CLI_router.main(): activates CLI_parser and displays the help section of the main parser showing which commands are accepted by the program.

The CLI main screen has 3 sections: systemtime management, product management and the commands to execute tasks regarding stock movements or generate reports. These sections will be described in the next chapters, where commands to execute tasks and commands generating reports will be discussed in seperate chapters.

### 2.2. Systemtime management

This section manipulates the time the program sees as "today" and contains 3 mutually exclusive optional arguments:
- report-time: activates functions_system.read_time() and returns the date saved in the "systemtime.txt" file.
```
>>> python superpy.py --report-time
System time is 2022-09-21 (21 September 2022)
```

- advance-time: activates functions_system.save_time(days=2, restore=False) and saves today's date + 2 days in the "systemtime.txt" file. The request was to be able to advance time by 2 days, hence the parser has action "store_const" and const = "2". If a client wants to be able to advance time with a self determined amount of days then the action and const should be removed from the parser.
NOTE: input of a negative integer is allowed and will save an older date to"systemtime.txt" when the function is called, but that date will be overwritten by toady's date when a new command is entered in the CLI (action 2 in chapter 2.1.).
```
>>> python superpy.py --advance-time
OK

>>> python superpy.py --report-time
System time is 2022-09-23 (23 September 2022)
```
- restore-time: activates functions_system.save_time(days=0, restore=True) and saves today's date in the "systemtime.txt" file.
```
>>> python superpy.py --restore-time
OK

>>> python superpy.py --report-time
System time is 2022-09-21 (21 September 2022)
```

### 2.3. Product management

This section determines which products are allowed in the store and contains 3 mutually exclusive optional arguments:
- product-list: activates functions_system.manage_products(product_list=True,add_product=None,delete_product=None), which in turn activates functions_system.read_products(). It will return a list of the products that are saved in the "products.csv" file.
```
>>> python superpy.py --product-list
Allowed product list is empty. Please add products using the --add-product command.
```
- add-product: activates functions_system.manage_products(product_list=False,add_product=[CLI input],delete_product=None) and adds the products entered in the CLI to the "products.csv" file.
```
ADD-PRODUCT EXAMPLE 1
>>> python superpy.py --add-product apple milk pear orange
4 products are added.

>>> python superpy.py --product-list
Allowed products:
apple
milk
pear
orange
```

```
ADD-PRODUCT EXAMPLE 2
>>> python superpy.py --add-product Orange pineapple chocolate porkchop
Product orange already exists.
3 products are added.

>>> python superpy.py --product-list
Allowed products:
apple
milk
pear
orange
pineapple
chocolate
porkchop
```

- delete-product: activates functions_system.manage_products(product_list=False,add_product=None,delete_product=[CLI input]) and removes the products entered in the CLI from the "products.csv" file.
```
DELETE-PRODUCT EXAMPLE 1
>>> python superpy.py --delete-product porkchop chickenwings
Product chickenwings is not in the list of products approved for sale in this store.
1 products are deleted.

>>> python superpy.py --product-list
Allowed products:
apple
milk
pear
orange
pineapple
chocolate
```

```
DELETE-PRODUCT EXAMPLE 2
>>> python superpy.py buy --product-name orange --amount 2 --price 0.36 --expiration-date 2022-09-22
OK

>>> python superpy.py --delete-product orange
Product orange will not be deleted: there still are 2 units in stock.
0 products are deleted.

>>> python superpy.py --product-list
Allowed products:
apple
milk
pear
orange
pineapple
chocolate
```

### 2.3. Commands to execute tasks

In the CLI "commands" section there are 3 commands that execute a task regarding stock movement: buy, sell and import-file. They are all (sub)parsers and have their own --help section giving more information on what other arguments are needed. 

##### 2.3.1. Buy command

When this command is entered the "get_method" method of the Action class is called. This method first runs functions_validation.validate_arguments() to check if all given arguments are within specified parameters and will return a message naming the errors plus exit the program if not all arguments pass the validation.
If validation is successful then the Action class method "buy" is called and the purchase is saved in the "purchases.csv" file (columns: ID, product_name, buy_date, buy_amount, buy_price_unit, expiration_date).

Arguments for this command:
- Product-name (required): the name of the product. Validation checks if the product is in the allowed product list.
- Price (required): the price per unit. Validation checks if it is a positive number and had no more than 2 decimals.
- Expiration-date (required): the date a product expires in the format YYYY-MM-DD. Validation checks if the date has the correct format, if it exists and if the product is not expired yet compared to today's date.
- Amount (optional): the amount of products that are bought. If no amount is entered it will default to 1. Parser checks if the value is an integer and validation checks if the integer is positive.


```
BUY EXAMPLE 1
>>> python superpy.py buy --product-name paer --amount -2 --price 0.364 --expiration-date 2022-09-31
Product is not in the list of products approved for sale in this store.
Amount needs to be a positive number.
Price can not have more than 2 decimals.
Expiration date does not exist.
```

```
BUY EXAMPLE 2
>>> python superpy.py buy --product-name pear --amount 7 --price 0.33 --expiration-date 2022-09-19
Expiration date has already passed.
```

```
BUY EXAMPLE 3
>>> python superpy.py buy --product-name pear --amount 7 --price 0.33 --expiration-date 2022-9-19
Expiration date is not correct. Format needs to be YYYY-MM-DD.
```

```
BUY EXAMPLE 4
>>> python superpy.py buy --product-name pear --amount 7 --price 0.33 --expiration-date 2022-09-22
OK

content purchases.csv file:
ID,product_name,buy_date,buy_amount,buy_price_unit,expiration_date
1,orange,2022-09-21,2,0.36,2022-09-22
2,pear,2022-09-21,7,0.33,2022-09-22
```

#### 2.3.2. Sell command

When this command is entered the "get_method" method of the Action class is called. This method first runs functions_validation.validate_arguments() to check if all given arguments are within specified parameters and will return a message naming the errors plus exit the program if not all arguments pass the validation.
If validation is successful then the Action class method "sell" is called and the sale is saved in the "sales.csv" file (columns: ID, buy_ID, product_name, sell_date, sell_amount, sell_price_unit).

Arguments for this command:
- Product-name (required): the name of the product. Validation checks if the product is in the allowed product list.
- Price (required): the selling price per unit. Validation checks if it is a positive number and had no more than 2 decimals.
- Amount (optional): the amount of products that are bought. If no amount is entered it will default to 1. Parser checks if the value is an integer and validation checks if the integer is positive and if there are enough products in stock for the sale.

```
SELL EXAMPLE 1
>>> python superpy.py sell --product-name paer --amount -2 --price 0.464
Product is not in the list of products approved for sale in this store.
Amount needs to be a positive number.
Price can not have more than 2 decimals.
```

```
SELL EXAMPLE 2
>>> python superpy.py sell --product-name orange --amount 40 --price 0.40
Not enough products in stock: only 2 available.
```

```
SELL EXAMPLE 3
>>> python superpy.py sell --product-name orange --amount 1 --price 0.40
OK

content sales.csv file:
ID,buy_ID,product_name,sell_date,sell_amount,sell_price_unit
1,1,orange,2022-09-21,1,0.4
```

#### 2.3.3. Import-file command

When this command is entered the "get_method" method of the ImportFromFile class is called. This method first runs the "convert_xlsx_to_csv" method in this class to convert the Excel file in a temporary CSV file. Next functions_validation.validate_file() is calles which invokes functions_validation.validate_arguments() to check if all given arguments on all lines of the file are within specified parameters. It will return a message naming the errors plus exit the program if not all arguments pass the validation.
If validation is successful then either the ImportFromFile class method "import_buy" of "import_sell" is called depending on given import-type. These methods call either the "buy" or "sell" method of class Action to save every line in the imported file.

Arguments for this command:
- Import-type (required): either "buy" or "sell" needs to be chosen. This argument determines which method in the class ImportFromFile is called ("import_buy" or "import_sell").
- File-path (required): the path to the file.
- File-name (required): the name of the file, including the ".xlsx" file extension.

Required headers in separate columns in the imported file (in random order):
- import-type "buy": product_name, price_unit, amount, expiration_date
- import-type "sell": product_name, price_unit, amount

```
IMPORT-FILE EXAMPLE 1 - PURCHASES WITH ERRORS
>>> python superpy.py import-file --import-type buy --file-path C:\myjunk\importfiles --file-name test-purchases-error.xlsx
Errors in line 1 of the file: ['Expiration date is not correct. Format needs to be YYYY-MM-DD.']
Errors in line 2 of the file: ['Product is not in the list of products approved for sale in this store.']
Errors in line 3 of the file: ['Expiration date does not exist.']
Errors in line 4 of the file: ['Amount needs to be a positive number.']
Errors in line 5 of the file: ['Price can not have more than 2 decimals.']
```

```
IMPORT-FILE EXAMPLE 2 - PURCHASES WITHOUT ERRORS
>>> python superpy.py import-file --import-type buy --file-path C:\myjunk\importfiles --file-name test-purchases-correct.xlsx
Import completed: 7 purchases transactions imported.

content purchases.csv file:
ID,product_name,buy_date,buy_amount,buy_price_unit,expiration_date
1,orange,2022-09-21,2,0.36,2022-09-22
2,pear,2022-09-21,7,0.33,2022-09-22
3,pineapple,2022-09-21,20,1.5,2022-10-07
4,orange,2022-09-21,8,0.4,2022-10-11
5,milk,2022-09-21,12,1.0,2022-11-18
6,chocolate,2022-09-21,9,0.6,2023-08-12
7,orange,2022-09-21,13,0.38,2022-10-12
8,pear,2022-09-21,19,0.2,2022-10-07
9,orange,2022-09-21,7,0.42,2022-10-14
```

```
IMPORT-FILE EXAMPLE 3 - SALES WITH ERRORS
>>> python superpy.py import-file --import-type sell --file-path C:\myjunk\importfiles --file-name test-sales-error.xlsx
Errors in line 1 of the file: ['Product is not in the list of products approved for sale in this store.']
Errors in line 2 of the file: ['Price can not have more than 2 decimals.']
Errors in line 3 of the file: ['Amount needs to be a positive number.']
```

```
IMPORT-FILE EXAMPLE 4 - SALES WITHOUT ERRORS
>>> python superpy.py import-file --import-type sell --file-path C:\myjunk\importfiles --file-name test-sales-correct.xlsx
Import completed: 3 sales transactions imported.

content sales.csv file:
ID,buy_ID,product_name,sell_date,sell_amount,sell_price_unit
1,1,orange,2022-09-21,1,0.4
2,3,pineapple,2022-09-21,9,1.8
3,1,orange,2022-09-21,1,0.6
4,4,orange,2022-09-21,8,0.6
5,7,orange,2022-09-21,3,0.6
6,5,milk,2022-09-21,2,1.15
```

### 2.4. Reports

The "report" command in the CLI "commands" section requires a subcommand to determine which report (subparsers of report) is wanted . Entering only the "report" command in the CLI will trigger an error message plus display the "report" help section.
The available reports are "revenue", "profit" and "inventory".
When entered in the CLI the "get_method" method of class Report is called. This method first runs functions_validation.validate_arguments() to check if all given arguments are within specified parameters and will return a message naming the errors plus exit the program if not all arguments pass the validation.
If validation is successful it will call the method corresponding to the name of the wanted report (the subcommand).

#### 2.4.1. Report revenue

To calculate the revenue this method calls functions_stock.sales() to determine which sales transactions have happened.
Depending on the given arguments the result is displayed in a single line or a table.

Required mutually exclusive arguments regarding the timeperiod of the report:
- Today: date used for calculating the revenue is the date saved in the "systemtime" file (obtained using functions_system.read_time()). 
- Yesterday: date used for calculating the revenue is the date saved in the "systemtime" file minus 1 day (obtained using functions_system.read_time(days=-1)).
- Date: date or timeperiod used for calculating the revenue is entered in the CLI. Format for 1 day is YYYY-MM-DD, format for a month is YYYY-MM and format for a year is YYYY. Validation checks if the format is correct and the requested day / month exists.

Optional mutually exclusive arguments:
- Product-name: adding this argument plus the name of a product will calculate the revenue of the requested product for the requested timeperiod.
- Per-product: adding this argument will generate a table with the revenue for the requested timeperiod split up in the different products.


```
REPORT REVENUE EXAMPLE 1
>>> python superpy.py report revenue --today
Revenue for today so far: € 26.10
```

```
REPORT REVENUE EXAMPLE 2
>>> python superpy.py report revenue --today --per-product
Revenue for today so far:
 ─────────────────────── 
  milk        €    2.30  
  orange      €    7.60  
  pineapple   €   16.20  
 ─────────────────────── 
  total       €   26.10  
 ─────────────────────── 
```

```
REPORT REVENUE EXAMPLE 3
>>> python superpy.py report revenue --today --product-name orange
Revenue of orange for today so far: € 7.60
```

```
REPORT REVENUE EXAMPLE 4 - ADVANCED TIME
>>> python superpy.py --advance-time
OK

>>> python superpy.py report revenue --yesterday --product-name orange
Revenue of orange for yesterday: € 0.00
```

```
REPORT REVENUE EXAMPLE 5 - ADVANCED TIME
>>> python superpy.py report revenue --date 2022-09-21 --product-name orange
Revenue of orange for 21 September 2022: € 7.60
```

```
REPORT REVENUE EXAMPLE 6 - ADVANCED TIME
>>> python superpy.py report revenue --date 2022-09
Revenue for September 2022: € 26.10
```

#### 2.4.2. Report profit

To calculate the profit this method calls functions_stock.sales() to determine which sales transactions have happened and calls functions_stock.purchases() to get the corresponding cost of sales.
All arguments are identical to 2.4.1. Report revenue.

```
REPORT PROFIT EXAMPLE 1
>>> python superpy.py report profit --today
Profit for today so far: € 5.54
```

```
REPORT PROFIT EXAMPLE 2
>>> python superpy.py report profit --date 2022 --per-product
Profit for 2022:
 ─────────────────────── 
  milk        €    0.30
  orange      €    2.54
  pineapple   €    2.70
 ───────────────────────
  total       €    5.54 
 ───────────────────────
```

#### 2.4.3. Report inventory

This method calls on functions_stock.determine_stock. That functions on it's turn calls on functions_stock.sales() and functions_stock.purchases() to extract all transactions. Only the transactions with a date older or equal to the requested date are taken into account. If for a "buy-ID" (generated when the purchase transaction is stored in the "purchases.csv" file) not all products are sold then that transaction is added to the stock list.

Required mutually exclusive arguments regarding the timeperiod of the report:
- Now: date used for determining stock is the date saved in the "systemtime" file (obtained using functions_system.read_time()). 
- Yesterday: date used for determining stock is the date saved in the "systemtime" file minus 1 day (obtained using functions_system.read_time(days=-1)).

Optional mutually exclusive arguments:
- Product-name: adding this argument plus the name of a product will generate a table with the stock of the requested product for the requested date.
- Per-product: adding this argument will generate a separate table for every product in stock with the stock of the requested date.

```
REPORT INVENTORY EXAMPLE 1
>>> python superpy.py report inventory --now
Stock on 21 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ chocolate    │      9 │  €    0.60 │ €       5.40 │ 2023-08-12      │
│ milk         │     10 │  €    1.00 │ €      10.00 │ 2022-11-18      │
│ orange       │     10 │  €    0.38 │ €       3.80 │ 2022-10-12      │
│ orange       │      7 │  €    0.42 │ €       2.94 │ 2022-10-14      │
│ pear         │      7 │  €    0.33 │ €       2.31 │ 2022-09-22      │
│ pear         │     19 │  €    0.20 │ €       3.80 │ 2022-10-07      │
│ pineapple    │     11 │  €    1.50 │ €      16.50 │ 2022-10-07      │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │     73 │            │ €      44.75 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
```

```
REPORT INVENTORY EXAMPLE 2
>>> python superpy.py report inventory --now --product-name orange
Stock on 21 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ orange       │     10 │  €    0.38 │ €       3.80 │ 2022-10-12      │
│ orange       │      7 │  €    0.42 │ €       2.94 │ 2022-10-14      │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │     17 │            │ €       6.74 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
```

```
REPORT INVENTORY EXAMPLE 3
>>> python superpy.py report inventory --yesterday --product-name orange
Stock on 20 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │      0 │            │ €       0.00 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
```

```
REPORT INVENTORY EXAMPLE 4
>>> python superpy.py report inventory --today --per-product
Stock on 21 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ pear         │      7 │  €    0.33 │ €       2.31 │ expired         │
│ pear         │     19 │  €    0.20 │ €       3.80 │ 2022-10-07      │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │     26 │            │ €       6.11 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
Stock on 21 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ pineapple    │     11 │  €    1.50 │ €      16.50 │ 2022-10-07      │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │     11 │            │ €      16.50 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
Stock on 21 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ milk         │     10 │  €    1.00 │ €      10.00 │ 2022-11-18      │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │     10 │            │ €      10.00 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
Stock on 21 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ chocolate    │      9 │  €    0.60 │ €       5.40 │ 2023-08-12      │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │      9 │            │ €       5.40 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
Stock on 21 September 2022:
┌──────────────┬────────┬────────────┬──────────────┬─────────────────┐
│ product name │ amount │  buy price │  total value │ expiration date │
│              │        │   per unit │              │                 │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ orange       │     10 │  €    0.38 │ €       3.80 │ 2022-10-12      │
│ orange       │      7 │  €    0.42 │ €       2.94 │ 2022-10-14      │
├──────────────┼────────┼────────────┼──────────────┼─────────────────┤
│ total        │     17 │            │ €       6.74 │                 │
└──────────────┴────────┴────────────┴──────────────┴─────────────────┘
```


