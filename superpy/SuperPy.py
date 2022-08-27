# Imports
import argparse, sys
import functions as SPfunction
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
        SPfunction.check_files()
        SPfunction.save_time()
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
            SPfunction.report_time()
        else:
            SPfunction.save_time(days=args.advance_time, restore=args.restore_time)

    else:
        validation = SPfunction.validate_arguments(
            price_unit=getattr(args, "price", None),
            amount=getattr(args, "amount", None),
            expiration_date=getattr(args, "expiration_date", None),
            manual_report_date=getattr(args, "manual_report_date", None),
        )

        if validation:
            print("\n".join(validation))
            exit(1)

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

            obj = SPclass.Action(
                ID=None,
                product_name=getattr(args, "product_name"),
                price_unit=getattr(args, "price"),
                amount=getattr(args, "amount"),
                expiration_date=getattr(args, "expiration_date", None),
            )
            obj.get_method(action=args.command)


if __name__ == "__main__":
    main()
