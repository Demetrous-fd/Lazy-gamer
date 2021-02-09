# -*- coding: utf-8 -*-

import sys
import click
import ctypes
import signal
from time import sleep
from scrapy import is_frozen
from console import console_menu
from game_collector import launch_bot, driver


def raise_console(console_toggle):
    """Brings up the Console Window."""
    if console_toggle:
        # Show console
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)
    else:
        # Hide console
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


def stop_browser_handler(signum, frame):
    print("Отправлен сигнал на завершение работы!")
    print("Через пару секунд программа закроется.")
    try:
        driver.quit()
    finally:
        sys.exit()


def silent_start():
    if is_frozen():
        raise_console(False)
    sleep(30)
    launch_bot()
    sys.exit()


@click.command()
@click.option("--silent", is_flag=True, help="Launch bot in background")
def main(silent):
    # Shutting down the bot when closing the program
    signal.signal(signal.SIGINT, stop_browser_handler)
    signal.signal(signal.SIGTERM, stop_browser_handler)
    if silent:
        silent_start()
    else:
        console_menu()


if __name__ == "__main__":
    main()
