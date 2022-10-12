import functions_system

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    functions_system.create_files()
    functions_system.save_time()

    # import of the CLI_router is not at the start of the file because it then imports a module that
    # calls a function that tries to open a file ("systemtime.txt") that does not exist yet,
    # since creation of the file happens later. Moving the 2 above calls to CLI_router module does not solve
    # it: it imports CLI_parser which also tries to open the "systemtime.txt" and do something with the content.
    # Another solution would be to add some code to "functions_system.read_time()" to call on "functions_system.save_time()"
    # if the file does not exist. Then the 2 above calls can be removed and all needed files are created when
    # modules are activated when imported. Chose not to do that, I don't want the files to be created
    # by a "fail save".

    import CLI_router

    CLI_router.main()


if __name__ == "__main__":
    main()
