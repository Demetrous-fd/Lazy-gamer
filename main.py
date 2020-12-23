#!/urs/bin/python3
#-*- coding: utf-8 -*-

import json
import datetime
from time import sleep
from browsers import Browser
from os.path import exists, getsize
from scrapy import get_info, get_users


def check_games(games):
    temp = []
    result = []
    data = json.load(open(r"data\left game.json"))
    for src in data:
        temp.append(src["game"])
    for game in games:
        if game["game"] in temp:
            pass
            # print("-" * 50)
            # print(f"{game['game']} имеется в библиотеке")
        else:
            result.append(game)

    # if len(temp) == len(result):
    #     print("-" * 50)
    return result


def send_to_check():
    games = []
    with open("data/last_game.json") as file:
        src = json.load(file)

    for game in src:
        if game["game"] != "Mystery Game":
            games.append({"game": game["game"], "link": game["link"]})

    if exists(r"data\left game.json") and getsize(r"data\left game.json") > 0:
        games = check_games(games)

    if len(games) > 0:
        get_game(games)


def get_game(games):
    try:
        driver.launch_browser(headless=True)
        print("-" * 50)

        for game in games:
            if game["game"] != "Mystery Game":
                driver.get_free_game(game["game"], game["link"])
    except Exception as ex:
        driver.get_screenshot("Crash" + datetime.datetime.today().strftime("%m-%d_%H-%M-%S"))
        print(ex)
    finally:
        sleep(3)
        driver.quit()


def main():
    get_info()
    if exists("data/cookies.pkl"):
        send_to_check()
    else:
        print("Пройдите авторизацию перед получением игры")
        sleep(3)
        driver.login()
        main()


if __name__ == "__main__":
    driver = Browser("yandex")
    main()
