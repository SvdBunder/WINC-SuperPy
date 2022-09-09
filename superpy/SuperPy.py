# Imports
import argparse, sys
import functions_system as SPFsystem
import CLI_parser as SPparser
import classes as SPclass


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():

    parser = SPparser.main_parser

    # starting the program using only "superpy.py" as command will trigger creating needed files, saving current date and print the help message
    if len(sys.argv) == 1:
        SPFsystem.create_files()
        SPFsystem.save_time()
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

            print(f"System time is {system_date} ({full_name_date}).")

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
        obj_file = SPclass.ImportFromFile(
            file_path=getattr(args, "file_path", None),
            file_name=getattr(args, "file_name", None),
        )
        method = "import_" + getattr(args, "type")
        return obj_file.get_method(action=method)

    elif args.command == "report":
        if args.report is None:
            print("ERROR: not specified which report is wanted.\n")
            SPparser.report_parser.print_help(sys.stderr)
            exit(1)
        else:
            obj_report = SPclass.Report(
                product_name=getattr(args, "product_name", None),
                report_date=(
                    getattr(args, "report_date")
                    if getattr(args, "report_date") is not None
                    else getattr(args, "manual_report_date")
                ),
                per_product=getattr(args, "per_product"),
            )

            return obj_report.get_method(action=args.report)

    else:
        obj_action = SPclass.Action(
            ID=None,
            product_name=getattr(args, "product_name"),
            price_unit=getattr(args, "price"),
            amount=getattr(args, "amount"),
            expiration_date=getattr(args, "expiration_date", None),
        )
        return obj_action.get_method(action=args.command)


if __name__ == "__main__":
    main()
