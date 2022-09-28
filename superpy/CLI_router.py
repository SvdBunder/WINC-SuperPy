import argparse, sys
import functions_system as SPFsystem
import CLI_parser as SPparser
import classes as SPclass


def main():
    parser = SPparser.main_parser

    # if no command is given will return help
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    # catching invalid command and returning help
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print("ERROR: chosen command does not exist.\n")
        parser.print_help(sys.stderr)
        exit(1)

    # calling the functions or classes
    if args.command is None:
        if args.report_time:
            system_date = SPFsystem.read_time(0)
            full_name_date = system_date.strftime("%d %B %Y")

            print(f"System time is {system_date} ({full_name_date})")

        elif (
            args.product_list
            or args.add_product is not None
            or args.delete_product is not None
        ):
            SPFsystem.manage_products(
                product_list=getattr(args, "product_list"),
                add_product=getattr(args, "add_product"),
                delete_product=getattr(args, "delete_product"),
            )

        else:
            SPFsystem.save_time(days=args.advance_time, restore=args.restore_time)

    elif args.command == "import-file":
        obj = SPclass.ImportFromFile(
            file_path=getattr(args, "file_path", None),
            file_name=getattr(args, "file_name", None),
        )
        action_wanted = "import_" + getattr(args, "type")

    elif args.command == "report":
        if args.report is None:
            print("ERROR: not specified which report is wanted.\n")
            SPparser.level1_report_parser.print_help(sys.stderr)
            exit(1)
        else:
            obj = SPclass.Report(
                product_name=getattr(args, "product_name", None),
                report_date=(
                    getattr(args, "report_date")
                    if getattr(args, "report_date") is not None
                    else getattr(args, "manual_report_date")
                ),
                per_product=getattr(args, "per_product"),
            )
            action_wanted = args.report

    else:
        obj = SPclass.Action(
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
