import argparse
import functions_system as SPFsystem

# -----------------------------------------------------------------------------------------
# CREATING PARENT PARSERS
# -----------------------------------------------------------------------------------------
#

# )

# PARENT PARSERS FOR SUBPARSERS BUY AND SELL
parent_parser_optional = argparse.ArgumentParser(add_help=False)
parent_parser_optional.add_argument(
    "--amount",
    default=1,
    type=int,
    help="Amount of products: a positive number without decimals. Default is 1.",
)
parent_parser_sell_required = argparse.ArgumentParser(add_help=False)
parent_parser_sell_required._action_groups[1].title = "required arguments"

parent_parser_sell_required.add_argument(
    "--product-name", help="Name of the product.", required=True
)
parent_parser_sell_required.add_argument(
    "--price",
    type=float,
    help="Price per unit: a positive number with 2 or less decimals.",
    required=True,
)


parent_parser_buy_required = argparse.ArgumentParser(
    add_help=False, parents=[parent_parser_sell_required]
)
parent_parser_buy_required._action_groups[1].title = "required arguments"
parent_parser_buy_required.add_argument(
    "--expiration-date",
    help="Date a product expires. Format used: YYYY-MM-DD.",
    required=True,
)

# PARENT PARSER FOR SUBPARSERS OF SUBPARSER REPORT
parent_report_optional = argparse.ArgumentParser(add_help=False)
parent_report_optional_exclusive = parent_report_optional.add_mutually_exclusive_group()
parent_report_optional_exclusive.add_argument(
    "--per-product",
    action="store_true",
    help="Reports per product, sorting on product name ascending by alphabetical order.",
)
parent_report_optional_exclusive.add_argument(
    "--product-name", help="Reports only the specified product."
)

# -----------------------------------------------------------------------------------------
# CREATING MAIN PARSER AND SUBPARSERS
# -----------------------------------------------------------------------------------------
#
# [level 0] MAIN PARSER

main_parser = argparse.ArgumentParser(
    description="Please enter a command plus the required arguments.",
    exit_on_error=False,
)
main_group_time = main_parser.add_argument_group(title="system time management")
main_exclusive_time = main_group_time.add_mutually_exclusive_group()
main_exclusive_time.add_argument(
    "--report-time", action="store_true", help="Show system time."
)
main_exclusive_time.add_argument(
    "--advance-time",
    action="store_const",
    const=2,
    default=0,
    help="Advances system time by 2 days.",
)
main_exclusive_time.add_argument(
    "--restore-time",
    action="store_true",
    help="Restores system time to current date.",
)

main_group_product = main_parser.add_argument_group(title="product management")
main_exclusive_product = main_group_product.add_mutually_exclusive_group()
main_exclusive_product.add_argument(
    "--product-list", action="store_true", help="Show a list of all allowed products."
)
main_exclusive_product.add_argument(
    "--add-product",
    nargs="+",
    help="Add one or more products (names divided by whitespace) to the list of allowed products.",
)
main_exclusive_product.add_argument(
    "--delete-product",
    nargs="+",
    help="Delete one or more products (names divided by whitespace) from the list of allowed products.",
)

# [level 1] SUBPARSERS TO MAIN PARSER

subparsers = main_parser.add_subparsers(dest="command")
buy_parser = subparsers.add_parser(
    "buy",
    help="Buying a product and adding to stock.",
    parents=[parent_parser_buy_required, parent_parser_optional],
)

sell_parser = subparsers.add_parser(
    "sell",
    help="Selling a product to a customer.",
    parents=[parent_parser_sell_required, parent_parser_optional],
)
import_parser = subparsers.add_parser(
    "import-file",
    help="Import purchase or sales transactions using a csv file. Required columns and headers: product_name | price_unit | amount (| expiration_date if it is a purchase).",
)
import_parser_group = import_parser.add_argument_group(title="required arguments")
import_parser_group.add_argument(
    "--import-type",
    help="Choose if the file contains purchases (buy) or sales (sell) transactions.",
    choices=["buy", "sell"],
    required=True,
    dest="type",
)
import_parser_group.add_argument(
    "--file-path", help="Path to the directory of the file.", required=True
)
import_parser_group.add_argument(
    "--file-name",
    help="Name of the file, including '.csv' file extension.",
    required=True,
)

report_parser = subparsers.add_parser(
    "report",
    help="Enter reporting subcommands. Add '-h' for a list of all available reports.",
    description="Please add one of the following commands to the report command, f.e. report profit.",
)

# [level 2] SUBPARSERS TO SUBPARSER 'REPORT'

report_subparsers = report_parser.add_subparsers(dest="report")

# [level 2] main - report - inventory
report_parser_inventory = report_subparsers.add_parser(
    "inventory",
    help="Generates a list of all products in inventory sorted by product name or of one product if a product name is added in the command. The list contains the product name, amount, buy price and expiration date.",
    parents=[parent_report_optional],
)


report_inventory_group = report_parser_inventory.add_argument_group(
    title="required: choose one of the following"
)
report_inventory_exclusive = report_inventory_group.add_mutually_exclusive_group(
    required=True
)
report_inventory_exclusive.add_argument(
    "--now",
    action="store_const",
    const=SPFsystem.read_time().strftime("%Y-%m-%d"),
    help="Report created based on saved system time.",
    dest="report_date",
)
report_inventory_exclusive.add_argument(
    "--yesterday",
    action="store_const",
    const=SPFsystem.read_time(days=-1).strftime("%Y-%m-%d"),
    help="Report created based on saved system time minus 1 day.",
    dest="report_date",
)

# [level 2] main - report - revenue
report_revenue = report_subparsers.add_parser(
    "revenue",
    parents=[parent_report_optional],
    help="Calculates total revenue or the revenue of one product if a product-name is added in the command. For a breakdown of the total revenue into the different products add '--per-product' to the command.",
)
report_revenue_group = report_revenue.add_argument_group(
    title="required: choose one of the following"
)
report_revenue_group_exlusive = report_revenue_group.add_mutually_exclusive_group(
    required=True
)
report_revenue_group_exlusive.add_argument(
    "--today",
    action="store_const",
    const=SPFsystem.read_time().strftime("%Y-%m-%d"),
    help="Report is created based on saved system time.",
    dest="report_date",
)
report_revenue_group_exlusive.add_argument(
    "--yesterday",
    action="store_const",
    const=SPFsystem.read_time(days=-1).strftime("%Y-%m-%d"),
    help="Report is created based on saved system time minus 1 day.",
    dest="report_date",
)
report_revenue_group_exlusive.add_argument(
    "--date",
    help="Report is created based on the entered time in one of the following formats:[YYYY-MM-DD] or [YYYY-MM] of [YYYY].",
    dest="manual_report_date",
)

# [level 2] main - report - profit
report_profit = report_subparsers.add_parser(
    "profit",
    parents=[parent_report_optional],
    help="Calculates total profit or the profit of one product if a product-name is added in the command. For a breakdown of the total profit into the different products add '--per product' to the command.",
)

report_profit_group = report_profit.add_argument_group(
    title="required: choose one of the following"
)
report_profit_group_exlusive = report_profit_group.add_mutually_exclusive_group(
    required=True
)
report_profit_group_exlusive.add_argument(
    "--today",
    action="store_const",
    const=SPFsystem.read_time().strftime("%Y-%m-%d"),
    help="Report is created based on saved system time.",
    dest="report_date",
)
report_profit_group_exlusive.add_argument(
    "--yesterday",
    action="store_const",
    const=SPFsystem.read_time(days=-1).strftime("%Y-%m-%d"),
    help="Report is created based on saved system time minus 1 day.",
    dest="report_date",
)
report_profit_group_exlusive.add_argument(
    "--date",
    help="Report is created based on the entered time in one of the following formats:[YYYY-MM-DD] or [YYYY-MM] of [YYYY].",
    dest="manual_report_date",
)
