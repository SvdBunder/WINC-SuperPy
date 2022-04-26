# Imports
import argparse
import csv
from datetime import date
import SuperPy_functions_time as SPtime
import SuperPy_functions_stock as SPstock


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    SPstock.check_files()
    SPtime.save_time()


if __name__ == "__main__":
    main()
