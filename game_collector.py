import sys
import json
import datetime
from time import sleep
from scrapy import get_info
from browsers import BrowserForWith, Browser
from itertools import groupby
from os.path import exists, getsize
from settings import update_setting, path, is_frozen, raise_console

PATH = path()


def silent_start():
    if is_frozen():
        raise_console(False)
    sleep(30)
    launch_bot()
    sys.exit()


def check_games(games):
    result = []
    if not exists(PATH + r"\data\left game.txt"):
        with open(PATH + r"\data\left game.txt", "w"):
            pass
    with open(PATH + r"\data\left game.txt") as file:
        data = file.read().splitlines()

    for game in games:
        if not game["game"] in data:
            result.append(game)

    return result


def send_to_check():
    games = []
    with open(PATH + r"\data\last_game.json") as file:
        src = json.load(file)

    for game in src:
        if game["game"] != "Mystery Game":
            games.append({"game": game["game"], "link": game["link"]})
        games = [el for el, _ in groupby(games)]

    if exists(PATH + r"\data\left game.txt") and getsize(PATH + r"\data\left game.txt") > 0:
        games = check_games(games)

    if len(games) > 0:
        get_game(games)


def get_game(games):
    try:
        with BrowserForWith() as driver:
            driver.launch_browser(headless=True)
            if driver.check_login():
                print("\n" * 2)
                print("-" * 50)

                for game in games:
                    if game["game"] != "Mystery Game":
                        driver.get_free_game(game["game"], game["link"])
                        print("-" * 50)
    except Exception as ex:
        #driver.get_screenshot("Crash" + datetime.datetime.today().strftime("%m-%d_%H-%M-%S"))
        print(ex)


def auth():
    with BrowserForWith() as driver:
        driver.login()


def update_browser():
    Browser().update_browser()


def test():
    with BrowserForWith() as driver:
        driver.launch_browser("https://www.epicgames.com/store/ru/", True, True)
        # driver.launch_browser("https://www.epicgames.com/store/ru/p/crysis-remastared", True, True)
        # driver.get_free_game("test", "https://www.epicgames.com/store/ru/p/metro-2033-redux")
        sleep(30)


def launch_bot():
    print("\n" * 50)
    update_setting("Other", "last_launch", datetime.datetime.today().strftime("%d.%m_%H:%M"))
    get_info()
    send_to_check()


if __name__ == '__main__':
    test()
