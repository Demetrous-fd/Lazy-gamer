from settings import get_setting, update_setting, disable_startup, enable_startup
import game_collector
import sys
import re


def input_int():
    while True:
        try:
            return int(input("Ввод: "))
        except ValueError:
            print("Введите число!\n")


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

        if "*" not in days and len(days.split(",")) != 7:
            print(f"""   Бот запускается в {get_setting("StartUp", "time")} по этим дням:""")
            print("   " + "-".join([days_list[day] for day in days.split(",")]))
        else:
            print(f"""   Бот запускается в {get_setting("StartUp", "time")} каждый день""")
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
            enable_startup()

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
            print("8. Каждый день")

            print("-" * 50)
            days = input("Ввод: ")

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
                days = "MON"

            update_setting("StartUp", "days", days)
            print("-" * 50)

            print("Введите время запуска бота:")
            print("-" * 50)
            time = input("Ввод: ")
            print(len(time))
            if len(time) == 1 or len(time) == 2:
                try:
                    if not int(time) < 0 or not int(time) > 23:
                        time += ":00"
                except Exception:
                    time = "14:00"
            elif not re.search("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", time):
                time = "14:00"
            update_setting("StartUp", "time", time)
            print("-" * 50)
            print("\n" * 50)

            disable_startup()
            update_setting("StartUp", "sometimes", "True")
            update_setting("StartUp", "everyday", "False")
            enable_startup(everyday=False)

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
    print("Выбран: " + get_setting("Settings", "browser").capitalize())
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

    game_collector.driver.update_browser()

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
            game_collector.launch_bot()
        elif choise == 1 and auth:
            print("\n" * 50)
            print("-" * 100)
            print("!!! Внимание !!!")
            print("1) Сейчас откроется окно браузера с формой авторизации в EpicGames Store")
            print("   Если окно браузера не открылось, перейдите по ссылке которая будет указана ниже.")
            print("2) Если на форме с авторизацией белый экран, перезагрузите страницу")
            print("3) Не закрывайте программу через крестик, используйте сочетание клавиш CTRL+C")
            print("4) При первом запуске откроется окно брандмауэра, для корректной работы бота дайте разрешение")
            print("-" * 100)
            input("Нажмите ENTER: ")
            print("-" * 100)
            game_collector.driver.login()
        elif choise == 2:
            print("\n" * 50)
            settings()
        elif choise == 3:
            print("\n" * 50)
            sys.exit()


def console_menu():
    draw_menu()
