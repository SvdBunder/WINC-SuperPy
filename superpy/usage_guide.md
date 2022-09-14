# SUPERPY USAGE GUIDE
---

## 1. General information

The program is written in python and uses Argparse for the command line interface (CLI).
It contains the following python files:
- SuperPy: main file initiating the program and determining actions based on CLI input.
- CLI_parser: creating the CLI-tool. Imported in: SuperPy.
- classes: several sections of the program with similar arguments are wrapped in classes. Imported in: SuperPy.
- functions_stock: functions to collect the saved sales and purchases data and determine stock. Imported in: classes, functions_system.
- functions_system: functions for system maintenance such as system time and allowed products. Imported in: SuperPy, CLI_parser, functions_validation.
- functions_validation: functions to validate the CLI input. Imported in: classes.

The purpose of this guide is to describe how the program operates, supplying ample examples plus results.
For demonstration purposes the GitHub repository includes 2 test import files (1 for sales and 1 for purchases) next to this guide, a readme.md and the aforementioned python files. *Only use these test files **BEFORE** the program has the go-live and delete the created sales and purchases CSV-files from the superpy-directory when done testing.*

## 2. Program operation

### 2.1. Getting started
CLI input:

```
>>> python superpy.py
```

This triggers 3 actions:
1. functions_system - create_file(): creates the CSV files for sales, purchases and products if they don't exist yet.
2. functions_system - save_time(): creates the txt file for saving system time if it does not exist and saves today's date if the date in the txt file is older than today.
3. CLI_parser: displays the help section of the main parser showing which commands are accepted by the program.

The CLI main screen can be divided into 3 sections: system time management, product management and the tasks / reports (aka 'commands'). These sections will be described in the next chapters.

