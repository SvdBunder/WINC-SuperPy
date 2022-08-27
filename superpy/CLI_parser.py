import argparse
import functions as SPfunctions

# -----------------------------------------------------------------------------------------
# CREATING PARENT PARSERS
# -----------------------------------------------------------------------------------------
#
# parent_parser with arguments shared by [level 1] parsers "sell" and "buy"
# parent_parser_task = argparse.ArgumentParser(add_help=False)
# parent_task_group = parent_parser_task.add_argument_group(title="Required arguments")
# parent_task_group.add_argument(
#    "--product-name", help="Name of the product.", required=True
# )
# parent_task_group.add_argument(
#    "--price",
#    type=float,
#    help="Price per unit: a positive number with 2 or less decimals.",
#    required=True,
# )
# parent_task_group.add_argument(
#    "--amount",
#    default=1,
#    type=int,
#    help="Amount of products: a positive number without decimals. Default is 1.",
# )

# TEST MET GROUPS ETCETERA
parent_parser_optional = argparse.ArgumentParser(add_help=False)
parent_parser_optional.add_argument(
    "--amount",
    default=1,
    type=int,
    help="Amount of products: a positive number without decimals. Default is 1.",
)
parent_parser_sell_required = argparse.ArgumentParser(add_help=False)

parent_parser_sell_required.add_argument(
    "--product-name", help="Name of the product.", required=True
)
parent_parser_sell_required.add_argument(
    "--price",
    type=float,
    help="Price per unit: a positive number with 2 or less decimals.",
    required=True,
)

parent_parser_sell_required._action_groups[1].title = "required arguments"
parent_parser_buy_required = argparse.ArgumentParser(
    add_help=False, parents=[parent_parser_sell_required]
)
parent_parser_buy_required.add_argument(
    "--expiration-date",
    help="Date a product expires. Format used: YYYY-MM-DD.",
    required=True,
)
parent_parser_buy_required._action_groups[1].title = "required arguments"

# parent_parser with arguments shared by the subparsers "revenue" and "profit" of subparser "report"
parent_parser_report = argparse.ArgumentParser(add_help=False)

parent_report_exclusive_optional = parent_parser_report.add_mutually_exclusive_group()
parent_report_exclusive_optional.add_argument(
    "--per-product", action="store_true", help="Reports per product."
)
parent_report_exclusive_optional.add_argument(
    "--product-name", help="Name of the product."
)

parent_report_exclusive_time = parent_parser_report.add_mutually_exclusive_group(
    required=True
)

parent_report_exclusive_time.add_argument(
    "--today",
    action="store_const",
    const=SPfunctions.report_time().strftime("%Y-%m-%d"),
    help="Report is created based on saved system time.",
    dest="report_date",
)
parent_report_exclusive_time.add_argument(
    "--yesterday",
    action="store_const",
    const=SPfunctions.report_time(days=-1).strftime("%Y-%m-%d"),
    help="Report is created based on saved system time minus 1 day.",
    dest="report_date",
)
parent_report_exclusive_time.add_argument(
    "--date",
    help="Report is created based on the entered time in one of the following formats:[YYYY-MM-DD] or [YYYY-MM] of [YYYY].",
    dest="manual_report_date",
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
main_exclusive_group = main_parser.add_argument_group(title="system time management")
main_exclusive_optionals = main_exclusive_group.add_mutually_exclusive_group()
main_exclusive_optionals.add_argument(
    "--report-time", action="store_true", help="Show system time."
)
main_exclusive_optionals.add_argument(
    "--advance-time",
    action="store_const",
    const=2,
    default=0,
    help="Advances system time by 2 days.",
)
main_exclusive_optionals.add_argument(
    "--restore-time",
    action="store_true",
    help="Restores system time to current date.",
)

# [level 1] SUBPARSERS TO MAIN PARSER

subparsers = main_parser.add_subparsers(dest="command")
buy_parser = subparsers.add_parser(
    "buy",
    help="Buying products and adding them to stock.",
    parents=[parent_parser_buy_required, parent_parser_optional],
)

sell_parser = subparsers.add_parser(
    "sell",
    help="Selling products to a customer.",
    parents=[parent_parser_sell_required, parent_parser_optional],
)

report_parser = subparsers.add_parser(
    "report",
    help="Enter reporting subcommands. Add '-h' for a list of all available reports.",
    description="Please add one of the following commands to the report command, f.e. report profit.",
)

# [level 2] SUBPARSERS TO SUBPARSER 'REPORT'

report_subparsers = report_parser.add_subparsers(dest="report")
report_parser_inventory = report_subparsers.add_parser(
    "inventory",
    help="Generates a list of all products in inventory or of one product if a product-name is added in the command.",
)
report_parser_inventory.add_argument("--product-name", help="Name of the product.")
report_inventory_exclusive = report_parser_inventory.add_mutually_exclusive_group(
    required=True
)
report_inventory_exclusive.add_argument(
    "--now",
    action="store_const",
    const=SPfunctions.report_time(),
    help="Report created based on saved system time.",
    dest="report_date",
)
report_inventory_exclusive.add_argument(
    "--yesterday",
    action="store_const",
    const=SPfunctions.report_time(days=-1),
    help="Report created based on saved system time minus 1 day.",
    dest="report_date",
)
report_parser_revenue = report_subparsers.add_parser(
    "revenue",
    parents=[parent_parser_report],
    help="Calculates total revenue or the revenue of one product if a product-name is added in the command. For a breakdown of the total revenue into the different products add '--per-product' to the command.",
)

report_parser_profit = report_subparsers.add_parser(
    "profit",
    parents=[parent_parser_report],
    help="Calculates total profit or the profit of one product if a product-name is added in the command. For a breakdown of the total profit into the different products add '--per product' to the command.",
)
