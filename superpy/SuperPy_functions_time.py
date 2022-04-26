# imports
from datetime import date, timedelta, datetime

# functions regarding saving and changing system date for SuperPy - to be called from SuperPy.py
def save_time(superpy_date=date.today()):
    with open("SuperPyDate.txt", "w") as file:
        file.write(superpy_date.strftime("%Y-%m-%d"))


def advance_time(days=0):
    with open("SuperPyDate.txt", "r") as file:
        saved_text = file.read()
        saved_date = datetime.strptime(saved_text, "%Y-%m-%d")

    date_advanced = saved_date + timedelta(days)
    save_time(superpy_date=date_advanced)
    return print("OK")


def restore_time():
    save_time()
    return print("Current date registered: OK")
