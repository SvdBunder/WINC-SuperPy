import argparse, sys
import functions_system
import CLI_parser
import classes


def main():
    parser = CLI_parser.main_parser

    # If no command is given will return help
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    # Catching invalid command and returning help
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print("ERROR: chosen command does not exist.\n")
        parser.print_help(sys.stderr)
        exit(1)

    # Calling functions and classes

    # The positional arguments : "report", "sell", "buy" and "import-file" are stored in "command"
    # If none of them are entered then code looks which optional argument is used and will execute the corresponding function.
    if args.command is None:
        # optional argument "--report-time"
        if args.report_time:
            system_date = functions_system.read_time(0)
            full_name_date = system_date.strftime("%d %B %Y")

            return print(f"System time is {system_date} ({full_name_date})")

        # optional arguments "--product-list", "--add-product" and "--delete-product"
        elif (
            args.product_list
            or args.add_product is not None
            or args.delete_product is not None
        ):
            return functions_system.manage_products(
                product_list=getattr(args, "product_list"),
                add_product=getattr(args, "add_product"),
                delete_product=getattr(args, "delete_product"),
            )

        # optional arguments "--advance-time" and "--restore-time"
        else:
            return functions_system.save_time(
                days=args.advance_time, restore=args.restore_time
            )

    # positional argument "import-file"; creates ImportFromFile classobject
    elif args.command == "import-file":
        obj = classes.ImportFromFile(
            file_path=getattr(args, "file_path", None),
            file_name=getattr(args, "file_name", None),
            file_type=getattr(args, "file_type", None),
        )
        action_wanted = "import_" + getattr(args, "transaction")

    # positional argument "report"; first part catches if user has not specified the wanted report and returns "report help",
    # second part creates Report classobject
    elif args.command == "report":
        if args.report is None:
            print("ERROR: not specified which report is wanted.\n")
            CLI_parser.level1_report_parser.print_help(sys.stderr)
            exit(1)
        else:
            obj = classes.Report(
                product_name=getattr(args, "product_name", None),
                report_date=(
                    getattr(args, "report_date")
                    if getattr(args, "report_date") is not None
                    else getattr(args, "manual_report_date")
                ),
                per_product=getattr(args, "per_product"),
            )
            action_wanted = args.report

    # positional argument "buy" or "sell"; creates Action classobject
    else:
        obj = classes.Action(
            ID=None,
            product_name=getattr(args, "product_name"),
            price_unit=getattr(args, "price"),
            amount=getattr(args, "amount"),
            expiration_date=getattr(args, "expiration_date", None),
        )

        action_wanted = args.command

    return obj.get_method(action=action_wanted)


if __name__ == "__main__":
    main()
