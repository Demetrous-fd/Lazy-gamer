import sys
import json
import datetime
from time import sleep
from scrapy import get_info
from browsers import Browser
from os.path import exists, getsize
from settings import update_setting, path, is_frozen, raise_console

PATH = path()
driver = Browser()


def silent_start():
    if is_frozen():
        raise_console(False)
    sleep(30)
    launch_bot()
    sys.exit()


def check_games(games):
    temp = []
    result = []
    data = json.load(open(PATH + r"\data\left game.json"))
    for src in data:
        temp.append(src["game"])
    for game in games:
        if game["game"] in temp:
            pass
        else:
            result.append(game)
    return result


def send_to_check():
    games = []
    with open(PATH + r"\data\last_game.json") as file:
        src = json.load(file)

    for game in src:
        if game["game"] != "Mystery Game":
            games.append({"game": game["game"], "link": game["link"]})

    if exists(PATH + r"\data\left game.json") and getsize(PATH + r"\data\left game.json") > 0:
        games = check_games(games)

    if len(games) > 0:
        get_game(games)


def get_game(games):
    try:
        driver.launch_browser(headless=True)
        if driver.check_login():
            print("\n" * 2)
            print("-" * 50)

            for game in games:
                if game["game"] != "Mystery Game":
                    driver.get_free_game(game["game"], game["link"])
                    print("-" * 50)
    except Exception as ex:
        driver.get_screenshot("Crash" + datetime.datetime.today().strftime("%m-%d_%H-%M-%S"))
        print(ex)
    finally:
        sleep(3)
        driver.quit()


def stop_browser_handler(signum, frame):
    print("Отправлен сигнал на завершение работы!")
    print("Через пару секунд программа закроется.")
    try:
        driver.quit()
    finally:
        sys.exit()


def test():
    driver.launch_browser("https://www.epicgames.com/store/ru/", True, True)
    sleep(30)
    driver.quit()


def launch_bot():
    print("\n" * 50)
    update_setting("Other", "last_launch", datetime.datetime.today().strftime("%d.%m_%H:%M"))
    get_info()
    send_to_check()


def stop_browser_handler(signum, frame):
    print("Отправлен сигнал на завершение работы!")
    print("Через пару секунд программа закроется.")
    try:
        driver.quit()
    finally:
        sys.exit()


if __name__ == '__main__':
    test()