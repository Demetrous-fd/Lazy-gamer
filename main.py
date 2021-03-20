# -*- coding: utf-8 -*-

import click
import win32api
from os import system
from console import console_menu
from game_collector import silent_start


def on_exit(signal_type):
    system(r"taskkill.exe /im chromedriver.exe /t /f")
    system(r"taskkill.exe /im msedgedriver.exe /t /f")


@click.command()
@click.option("--silent", is_flag=True, help="Launch bot in background")
def main(silent):
    win32api.SetConsoleCtrlHandler(on_exit, True)
    if silent:
        silent_start()
    else:
        console_menu()


if __name__ == "__main__":
    main()
