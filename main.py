# -*- coding: utf-8 -*-

import re
import sys
import json
import winreg
import datetime
import subprocess
from time import sleep
from browsers import Browser
from os.path import exists, getsize
from settings import get_setting, update_setting
from scrapy import get_info, is_frozen, get_path_pythonw

PATH = get_setting("Settings", "path")


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


def launch_bot():
    print("\n" * 50)
    update_setting("Other", "last_launch", datetime.datetime.today().strftime("%d.%m_%H:%M"))
    get_info()
    send_to_check()


def input_int():
    while True:
        try:
            return int(input("Ввод: "))
        except ValueError:
            print("Введите число!\n")


def add_startup(everyday=True):
    path = PATH
    pythonw_path = get_path_pythonw()
    if everyday:
        if is_frozen():
            path += "\\LazyGamer.exe"
            command = f'"{path}" -silent'

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                winreg.KEY_WRITE) as key:

                winreg.SetValueEx(key, "LazyGamer", 0, winreg.REG_SZ, command)

        else:
            path += "\\main.py"
            command = f'''"{pythonw_path}" "{path}" -silent'''
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "LazyGamerPy", 0, winreg.REG_SZ, command)
    else:
        days = get_setting("StartUp", "days")
        time = get_setting("StartUp", "time")
        if is_frozen():
            path += "\\LazyGamer.exe"
            command = f'"{path}" -silent'
            subprocess.Popen(['schtasks.exe', '/create', '/TN', "LazyGamer", "/tr", command, "/SC", "weekly", "/d", days,
                              "/st", time], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            path += "\\main.py"
            command = f'''"{pythonw_path}" "{path}" -silent'''
            subprocess.Popen(['schtasks.exe', '/create', '/TN', "LazyGamerPy", "/tr", command, "/SC", "weekly", "/d", days,
                              "/st", time], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def disable_startup():

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                        winreg.KEY_WRITE) as key:
        try:
            if is_frozen():
                winreg.DeleteValue(key, "LazyGamer")

            else:
                winreg.DeleteValue(key, "LazyGamerPy")
        except FileNotFoundError:
            pass

    subprocess.Popen(['schtasks.exe', '/delete', '/TN', "LazyGamer", "/F"], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    subprocess.Popen(['schtasks.exe', '/delete', '/TN', "LazyGamerPy", "/F"], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


def startup():
    days_list = {
        "MON": "Понедельник",
        "TUE": "Вторник",
        "WED": "Среда",
        "THU": "Четверг",
        "FRI": "Пятница",
        "SAT": "Субота",
        "SUN": "Воскресенье"
    }
    print("-" * 50)
    if get_setting("StartUp", "everyday") == "True":
        update_setting("StartUp", "sometimes", "False")
        print("   Бот запускается каждый день")
        print("-" * 50)

    elif get_setting("StartUp", "sometimes") == "True":
        update_setting("StartUp", "everyday", "False")
        days = get_setting("StartUp", "days")

        print(f"""   Бот запускается в {get_setting("StartUp", "time")} по этим дням:""")
        print("   " + "-".join([days_list[day] for day in days.split(",")]))
        print("-" * 50)
    else:
        print("   Автозапуск не настроен")
        print("-" * 50)

    print("1. Автозапуск при включении пк")
    print("2. Автозапуск по определённым дням")
    print("3. Отключить автозапуск")
    print("4. Назад")

    print("-" * 50)
    choise = input_int()
    print("-" * 50)
    print("\n" * 50)

    if choise == 1:
        print("-" * 50)
        status = get_setting("StartUp", "everyday") == "True"
        if status:
            print("1. Выключить")
        else:
            print("1. Включить")
        print("2. Назад")

        print("-" * 50)
        choise = input_int()
        print("-" * 50)
        print("\n" * 50)

        if choise == 1 and status:
            update_setting("StartUp", "everyday", "False")
            disable_startup()
        elif choise == 1 and not status:
            disable_startup()
            update_setting("StartUp", "everyday", "True")
            update_setting("StartUp", "sometimes", "False")
            add_startup()

        startup()

    elif choise == 2:
        print("-" * 50)
        status = get_setting("StartUp", "sometimes") == "True"
        if status:
            print("1. Выключить")
        else:
            print("1. Включить")
        print("2. Изменить дни запуска")
        print("3. Назад")

        print("-" * 50)
        choise = input_int()
        print("-" * 50)

        if choise == 1 and status:
            update_setting("StartUp", "sometimes", "False")
            disable_startup()
        elif choise == 1 and not status or choise == 2:
            print("Выберите дни запуска бота через запятую:")
            print("1. Понедельник")
            print("2. Вторник")
            print("3. Среда")
            print("4. Четверг")
            print("5. Пятница")
            print("6. Субота")
            print("7. Воскресенье")

            print("-" * 50)
            days = input("Ввод: ")

            days_list = {
                "1": "MON",
                "2": "TUE",
                "3": "WED",
                "4": "THU",
                "5": "FRI",
                "6": "SAT",
                "7": "SUN"
            }

            days = "".join(days.split(" "))
            days = ",".join(sorted(days.split(",")))
            days = ",".join([days_list[day] for day in days.split(",") if day != "" and re.search(r"\d", day)])
            if days == "":
                days = "MON"

            update_setting("StartUp", "days", days)
            print("-" * 50)

            print("Введите время запуска бота в таком формате 13:37")
            print("-" * 50)
            time = input("Ввод: ")
            if not re.search(r"/^([01][0-9]|2[0-3]):([0-5][0-9])$/", time):
                time = "13:37"
            update_setting("StartUp", "time", time)
            print("-" * 50)
            print("\n" * 50)

            if choise != 2:
                disable_startup()
                update_setting("StartUp", "sometimes", "True")
                update_setting("StartUp", "everyday", "False")
                add_startup(everyday=False)

        print("\n" * 50)
        startup()

    elif choise == 3:
        update_setting("StartUp", "everyday", "False")
        update_setting("StartUp", "sometimes", "False")
        disable_startup()
        startup()

    else:
        settings()


def set_browser():
    print("\n" * 50)
    print("-" * 50)
    print("Выбран: " + get_setting("Settings", "browser"))
    print("-" * 50)
    print("Выберите браузер:")
    print("1. Chrome")
    print("2. Edge")
    print("3. Назад")

    print("-" * 50)
    browser = input_int()
    print("-" * 50)

    if browser == 1:
        update_setting("Settings", "browser", "chrome")
    elif browser == 2:
        update_setting("Settings", "browser", "edge")
    else:
        print("\n" * 50)
        settings()

    set_browser()


def settings():
    print("-" * 50)
    print("   Настройки")
    print("-" * 50)
    print("1. Изменить браузер, которым пользуется бот")
    print("2. Автозапуск")
    print("3. Назад")
    print("-" * 50)
    choise = input_int()
    print("-" * 50)
    print()

    if choise == 1:
        set_browser()

    elif choise == 2:
        print("\n" * 50)
        startup()
    else:
        draw_menu()


def draw_logo():
    print("\n" * 100)
    print(r"""
        __                      ______                         
       / /   ____ _____  __  __/ ____/___ _____ ___  ___  _____
      / /   / __ `/_  / / / / / / __/ __ `/ __ `__ \/ _ \/ ___/
     / /___/ /_/ / / /_/ /_/ / /_/ / /_/ / / / / / /  __/ /    
    /_____/\__,_/ /___/\__, /\____/\__,_/_/ /_/ /_/\___/_/     
                      /____/                                   """)
    print("\n" * 2)


def draw_menu():
    while True:
        draw_logo()
        auth = get_setting("Settings", "auth") == "False"

        if auth:
            print("-" * 50)
            print("1. Пройдите авторизацию перед работой с ботом")
            print("2. Настройки")
            print("3. Выход")
            print("-" * 50)
        else:
            print("-" * 20)
            if len(get_setting("Other", "last_launch")) == 0:
                print("1. Запустить бота")
            else:
                last_launch = " ".join(get_setting("Other", "last_launch").split("_"))
                print(f"""1. Запустить бота (Последний запуск: {last_launch})""")
            print("2. Настройки")
            print("3. Выход")
            print("-" * 20)

        choise = input_int()

        if auth:
            print("-" * 50)
        else:
            print("-" * 20)

        print("\n")

        if choise == 1 and not auth:
            launch_bot()
        elif choise == 1 and auth:
            print("\n" * 50)
            print("-" * 50)
            print("Внимание")
            print("После нажития ENTER:\nОткроется окно браузера с формой авторизации в EpicGames Store")
            print("Если окно браузера не открылось, перейдите по ссылке которая будет указана ниже")
            print("-" * 50)
            input("Ввод: ")
            print("-" * 50)
            driver.login()
        elif choise == 2:
            print("\n" * 50)
            settings()
        elif choise == 3:
            print("\n" * 50)
            exit(0)


def console_menu():
    draw_menu()


def main():
    print(sys.argv)
    try:
        if sys.argv[-1] == "-silent":
            try:
                launch_bot()
            except Exception:
                driver.quit()
        else:
            console_menu()
    except Exception:
        console_menu()


if __name__ == "__main__":
    driver = Browser()  # chrome or edge
    main()
