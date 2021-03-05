# -*- coding: utf-8 -*-

import click
import signal
from console import console_menu
from game_collector import silent_start, stop_browser_handler



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
