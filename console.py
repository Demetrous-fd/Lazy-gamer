from settings import get_setting, update_setting, disable_startup, enable_startup
from manager import browser_exists
from colorama import Fore, init, Style, Back
import game_collector
import sys
import re

init()


def input_int(text="    >>> "):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Введите число!\n")


def startup():
    status = get_setting("StartUp", "startup", True)
    if not get_setting("Settings", "first_start", True):
        print(("-" * 60).center(66))
        if status:
            print("\t1. Выключить")
        else:
            print("\t1. Включить")
        print("\t2. Изменить дни запуска")
        print("\t3. Назад")

        print(("-" * 60).center(66))
        choise = input_int()
        print("\n" * 50)
        print(("-" * 60).center(66))
    else:
        choise = 1

    if choise == 1 and status:
        update_setting("StartUp", "startup", "False")
        disable_startup()
    elif choise == 1 and not status or choise == 2:
        print("Выберите дни запуска бота через запятую".center(66))
        print(("-" * 60).center(66))
        print("\t1. Понедельник")
        print("\t2. Вторник")
        print("\t3. Среда")
        print("\t4. Четверг")
        print("\t5. Пятница")
        print("\t6. Субота")
        print("\t7. Воскресенье")
        print("\t8. Каждый день")

        print(("-" * 60).center(66))
        days = input("    (Пятница) >>> ")

        days_list = {
            "1": "MON",
            "2": "TUE",
            "3": "WED",
            "4": "THU",
            "5": "FRI",
            "6": "SAT",
            "7": "SUN",
            "8": "*"
        }
        if "*" not in days:
            days = "".join(days.split(" "))
            days = ",".join(sorted(days.split(",")))
            days = ",".join([days_list[day] for day in days.split(",") if day != "" and re.search(r"\d", day)])
        if days == "":
            days = "FRI"

        update_setting("StartUp", "days", days)
        print(("-" * 60).center(66))

        print("Введите время запуска бота".center(66))
        print(("-" * 60).center(66))
        time = input("    (14:00) >>> ")
        if len(time) == 1 or len(time) == 2:
            try:
                if not int(time) < 0 or not int(time) > 23:
                    time += ":00"
            except Exception:
                time = "14:00"
        elif not re.search("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", time):
            time = "14:00"
        update_setting("StartUp", "time", time)
        print(("-" * 60).center(66))
        print("\n" * 50)

        disable_startup()
        update_setting("StartUp", "startup", "True")
        enable_startup()

    else:
        print("\n" * 50)


def startup_menu():
    days_list = {
        "MON": "Понедельник",
        "TUE": "Вторник",
        "WED": "Среда",
        "THU": "Четверг",
        "FRI": "Пятница",
        "SAT": "Субота",
        "SUN": "Воскресенье"
    }

    print(("-" * 60).center(66))

    if get_setting("StartUp", "startup", True):
        days = get_setting("StartUp", "days")

        if "*" not in days and len(days.split(",")) != 7:
            print(f"""Бот запускается в {get_setting("StartUp", "time")} по этим дням:""".center(66))
            print(("-".join([days_list[day] for day in days.split(",")])).center(66))
        else:
            print(f"""Бот запускается в {get_setting("StartUp", "time")} каждый день""".center(66))
        print(("-" * 60).center(66))
    else:
        print("Автозапуск не настроен".center(66))
        print(("-" * 60).center(66))

    print("\t1. Автозапуск")
    print("\t2. Отключить автозапуск")
    print("\t3. Назад")

    print(("-" * 60).center(66))
    choise = input_int()
    print(("-" * 60).center(66))
    print("\n" * 50)

    if choise == 1:
        startup()
        startup_menu()

    elif choise == 2:
        update_setting("StartUp", "startup", "False")
        disable_startup()

        startup_menu()

    else:
        print("\n" * 50)
        settings()


def set_browser():
    print("\n" * 50)
    print(("-" * 60).center(66))
    print(("Выбран: " + get_setting("Settings", "browser").capitalize()).center(66))
    print(("-" * 60).center(66))
    print("Выберите браузер".center(66))
    print(("-" * 60).center(66))
    print(f"\t1. {Fore.GREEN}Google Chrome{Fore.RESET}") if browser_exists("Google Chrome") else print(f"\t1. {Fore.RED}Google Chrome (Не установлен){Fore.RESET}")
    print(f"\t2. {Fore.GREEN}Microsoft Edge{Fore.RESET}") if browser_exists("Microsoft Edge") else print(f"\t2. {Fore.RED}Microsoft Edge (Не установлен){Fore.RESET}")
    print(f"\t3. {Fore.YELLOW}Назад{Fore.RESET}")
    print(("-" * 60).center(66))
    browser = input_int()
    print(("-" * 60).center(66))

    if browser == 1 and browser_exists("Google Chrome"):
        update_setting("Settings", "browser", "chrome")
    elif browser == 2 and browser_exists("Microsoft Edge"):
        update_setting("Settings", "browser", "edge")
    else:
        print("\n" * 50)
        settings()

    set_browser()


def settings():
    print(("-" * 60).center(66))
    print("Настройки".center(66))
    print(("-" * 60).center(66))
    print("\t1. Изменить браузер, которым пользуется бот")
    print("\t2. Автозапуск")
    print("\t3. Назад")
    print(("-" * 60).center(66))
    choise = input_int()
    print(("-" * 60).center(66))
    print()

    if choise == 1:
        set_browser()

    elif choise == 2:
        print("\n" * 50)
        startup_menu()
    else:
        draw_menu()


def draw_logo():
    print("\n" * 50)
    print(Style.BRIGHT + r"""
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
        auth = get_setting("Settings", "auth", True)

        if not auth:
            print(("-" * 60).center(66))
            print("\t1. Пройдите авторизацию перед работой с ботом")
            print("\t2. Настройки")
            print(f"\t3. Выход")
            print(("-" * 60).center(66))
        else:
            print(("-" * 60).center(66))
            if len(get_setting("Other", "last_launch")) == 0:
                print("\t1. Запустить бота")
            else:
                last_launch = " ".join(get_setting("Other", "last_launch").split("_"))
                print(f"""\t1. Запустить бота (Последний запуск: {last_launch})""")
            print("\t2. Настройки")
            print("\t3. Выход")
            print(("-" * 60).center(66))

        choise = input_int()

        if auth:
            print(("-" * 60).center(66))

        print("\n")

        if choise == 1 and auth:
            game_collector.launch_bot()
        elif choise == 1 and not auth:
            print("\n" * 50)
            print(("-" * 101).center(100))
            print(Fore.RED + "!!! Внимание !!!".center(100) + Fore.RESET)
            print("\t1) Сейчас откроется окно браузера с формой авторизации в EpicGames Store")
            print("\t2) Если окно браузера не открылось, перейдите по ссылке которая будет указана ниже.")
            print("\t3) Если на форме с авторизацией белый экран, перезагрузите страницу")
            print("\t4) При первом запуске откроется окно брандмауэра, для корректной работы бота дайте разрешение")
            print(("-" * 101).center(100))
            input("Нажмите ENTER".center(100))
            print("\n" * 50)
            game_collector.auth()
        elif choise == 2:
            print("\n" * 50)
            settings()
        elif choise == 3:
            print("\n" * 50)
            sys.exit()


def first_start():
    def title():
        print("\n" * 50)
        draw_logo()
        print(("-" * 60).center(66))
        print("Первоначальная настройка бота".center(66))
        print(("-" * 60).center(66))

    def step_1():
        """Select browser"""
        print("Выберите один из браузеров".center(66))
        print(("-" * 60).center(66))
        print(f"\t1. {Fore.GREEN}Google Chrome{Fore.RESET}") if browser_exists("Google Chrome") else \
            print(f"\t1. {Fore.RED}Google Chrome (Не установлен){Fore.RESET}")

        print(f"\t2. {Fore.GREEN}Microsoft Edge{Fore.RESET}") if browser_exists("Microsoft Edge") else \
            print(f"\t2. {Fore.RED}Microsoft Edge (Не установлен){Fore.RESET}")

        print(("-" * 60).center(66))
        browser = input_int()

        if browser == 1 and browser_exists("Google Chrome"):
            update_setting("Settings", "browser", "chrome")
        elif browser >= 2 and browser_exists("Microsoft Edge"):
            update_setting("Settings", "browser", "edge")

    def step_2():
        """Enable StartUp"""
        print(("-" * 60).center(66))
        print(f"Настройка автозапуска".center(66))
        print(("-" * 60).center(66))

        print(f"\t1. {Fore.GREEN}Включить{Fore.RESET}")
        print(f"\t2. {Fore.YELLOW}Пропустить настройку автозапуска{Fore.RESET}")
        print(("-" * 60).center(66))

        if input_int() == 1:
            print(("-" * 60).center(66))
            startup()
        else:
            print(("-" * 60).center(66))

        print("Настройка завершена".center(66))
        print(("-" * 60).center(66))

        update_setting("Settings", "first_start", "False")

    def main():
        title()
        step_1()
        step_2()

    main()


def console_menu():
    if get_setting("Settings", "first_start", True):
        first_start()
    draw_menu()


if __name__ == '__main__':
    # first_start()
    console_menu()
