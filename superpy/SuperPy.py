import functions_system as SPFsystem

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    SPFsystem.create_files()
    SPFsystem.save_time()

    import CLI_router as SProuter

    SProuter.main()


if __name__ == "__main__":
    main()
