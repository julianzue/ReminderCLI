import click
from colorama import Fore, Style, init
import time
from rich.table import Table
from rich.console import Console
import os
import datetime


c = Fore.CYAN
r = Fore.RED
y = Fore.YELLOW
re = Fore.RESET


def is_time_future(hour, minute):

  today = datetime.date.today()
  given_time = datetime.datetime(today.year, today.month, today.day, hour, minute) + datetime.timedelta(minutes=1)

  return given_time >= datetime.datetime.now()


def time_left(hour, minute):

  today_left = datetime.date.today()
  given_time_left = datetime.datetime(today_left.year, today_left.month, today_left.day, hour, minute) + datetime.timedelta(minutes=1)

  time_left_full = given_time_left - datetime.datetime.now()
  time_left_out = str(time_left_full).split(":")[0] + ":" + str(time_left_full).split(":")[1]

  return str(time_left_out)


@click.group
def commandlist():
    pass


@click.command()
@click.option("-n", "--name", prompt="Enter name of reminder", help="Define name of reminder")
@click.option("-t", "--target", prompt="Enter target-time of reminder (HH:MM)", help="Define target-time of reminder (HH:MM)")
def new(name, target):

    time_added = time.strftime("%Y-%m-%d %H:%M:%S")

    with open("reminders.txt", "a") as reminders:
        reminders.write(time_added + " | " + target + " | " + name + "\n")

    click.echo(f"{c}[*] {re}Successfully added {c}{name} {re}to {c}reminders.txt{re}!")


@click.command()
def show():
    
    try:

        table = Table(title="All Reminders", show_lines=True)

        table.add_column("No")
        table.add_column("Date Added")
        table.add_column("Target Time")
        table.add_column("Name", width=40)

        with open("reminders.txt", "r") as reminders:
            for index, line in enumerate(reminders.readlines(), 1):
                part = line.strip("\n").split(" | ")

                table.add_row("{:02d}".format(index), part[0], part[1], part[2])

        console = Console()
        console.print(table)                

    except:
        click.echo(f"{r}[!] {re}File {r}reminders.txt{re} not found!")


@click.command()
def live():

    try:

        saved_time = ""

        while True:

            all_done = True

            try:
                os.system("clear")

                table = Table(title="Open Reminders for Today", show_lines=True)

                table.add_column("No")
                table.add_column("Date Added")
                table.add_column("Target Time")
                table.add_column("Time Left")
                table.add_column("Name", width=40)

                with open("reminders.txt", "r") as reminders:
                    for index, line in enumerate(reminders.readlines(), 1):
                        part = line.strip("\n").split(" | ")

                        mins = int(part[1].split(":")[1])
                        hrs = int(part[1].split(":")[0])

                        if is_time_future(hrs, mins):

                            all_done = False

                            if part[1] == time.strftime("%H:%M") and saved_time != time.strftime("%H:%M"):
                                saved_time = time.strftime("%H:%M")
                                os.system("notify-send " + part[1] + " " + part[2])

                            if part[1] == time.strftime("%H:%M"):
                                table.add_row("{:02d}".format(index), part[0], part[1], time_left(hrs, mins), part[2], style="cyan")
                            else:
                                table.add_row("{:02d}".format(index), part[0], part[1], time_left(hrs, mins), part[2])

                if all_done:
                    click.echo(f"{c}[*] {re}All done. Congratulations!")

                else:
                    console = Console()
                    console.print(table)

                #if part[1] == time.strftime("%H:%M"):
                #    print("")
                #    click.echo("[*] " + part[1] + ": " + part[2])

                print("")
                click.echo("Refresh: " + time.strftime("%Y-%m-%d %H:%M:%S"))
                click.echo("Close:   Ctrl+C") 

                time.sleep(10) 

            except KeyboardInterrupt:
                break          

    except Exception as err:
        click.echo(f"{r}[!] {re}File {r}reminders.txt{re} not found!")
        click.echo(err)


@click.command()
@click.option("-i", "--index", prompt="Enter index to delete line", help="Set index of reminder line to delete", type=int)
def delete(index):
    
    try:

        with open("reminders.txt", "r") as f:
            reminders_list = f.read().splitlines()
            reminders_list.pop(index - 1)

        with open("reminders.txt", "w") as f:
            f.write("\n".join(reminders_list))
            f.write("\n")

    except:
        click.echo(f"{r}[!] {re}File {r}reminders.txt{re} not found!")


commandlist.add_command(new)
commandlist.add_command(show)
commandlist.add_command(live)
commandlist.add_command(delete)


if __name__ == "__main__":
    commandlist()