from scrapy import path, is_frozen, get_path_pythonw
from manager import browser_exists
from os.path import exists
from os import mkdir
import configparser
import subprocess
import ctypes

PATH = path()
PATH_TO_SETTINGS = PATH + "\\data\\settings.ini"
OLD_OPTIONS = {
    "StartUp": ("everyday", "sometimes")
}
NEW_OPTIONS = {
    "StartUp": [["startup", "False"]],
    "Settings": [["first_start", "False"]]
}


def create_config():
    if not exists(path() + "\\data"):
        mkdir(path() + "\\data")

    config = configparser.ConfigParser()

    config.add_section("Settings")

    if browser_exists("Google Chrome"):
        config.set("Settings", "browser", "chrome")
    elif browser_exists("Microsoft Edge"):
        config.set("Settings", "browser", "edge")
    else:
        config.set("Settings", "browser", "NULL")
    config.set("Settings", "auth", "False")
    config.set("Settings", "first_start", "True")

    config.add_section("StartUp")
    config.set("StartUp", "startup", "False")
    config.set("StartUp", "days", "NULL")
    config.set("StartUp", "time", "NULL")

    config.add_section("WebDriver")
    config.set("WebDriver", "driver_manager", "True")
    config.set("WebDriver", "chrome_driver_path", "NULL")
    config.set("WebDriver", "msedge_driver_path", "NULL")

    config.add_section("Other")
    config.set("Other", "last_launch", "")

    with open(PATH_TO_SETTINGS, "w", encoding="utf8") as config_file:
        config.write(config_file)


def get_config():
    if not exists(PATH_TO_SETTINGS):
        create_config()

    config = configparser.ConfigParser()
    config.read(PATH_TO_SETTINGS, encoding="utf8")
    return config


def get_setting(section, setting, bool_val=False):
    config = get_config()
    if bool_val:
        value = config.getboolean(section, setting)
    else:
        value = config.get(section, setting)
    return value


def update_setting(section, setting, value):
    config = get_config()
    config.set(section, setting, value)
    with open(PATH_TO_SETTINGS, "w", encoding="utf8") as config_file:
        config.write(config_file)


def remove_old_options():
    config = get_config()
    for section in OLD_OPTIONS:
        for option in OLD_OPTIONS[section]:
            if config.has_option(section, option):
                if section == "StartUp" and config.getboolean(section, option):
                    NEW_OPTIONS["StartUp"][0][1] = "True"
                config.remove_option(section, option)
    with open(PATH_TO_SETTINGS, "w", encoding="utf8") as file:
        config.write(file)


def set_new_options():
    config = get_config()
    for section in NEW_OPTIONS:
        for option in NEW_OPTIONS[section]:
            config.set(section, option[0], option[1]) if not config.has_option(section, option[0]) else None
    with open(PATH_TO_SETTINGS, "w", encoding="utf8") as file:
        config.write(file)


def enable_startup():
    path = PATH
    days = get_setting("StartUp", "days")
    time = get_setting("StartUp", "time")
    days_list = {
        "MON": "<Monday />",
        "TUE": "<Tuesday />",
        "WED": "<Wednesday />",
        "THU": "<Thursday />",
        "FRI": "<Friday />",
        "SAT": "<Saturday />",
        "SUN": "<Sunday />"
    }
    xml = r'''<?xml version="1.0" encoding="UTF-16"?>
    <Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
      <RegistrationInfo>
        <URI>\{0}</URI>
      </RegistrationInfo>
      <Triggers>
        <CalendarTrigger>
          <StartBoundary>2021-04-11T{1}:00</StartBoundary>
          <Enabled>true</Enabled>
          <ScheduleByWeek>
            <DaysOfWeek>
              {2}
            </DaysOfWeek>
            <WeeksInterval>1</WeeksInterval>
          </ScheduleByWeek>
        </CalendarTrigger>
      </Triggers>
      <Settings>
        <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
        <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
        <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
        <AllowHardTerminate>true</AllowHardTerminate>
        <StartWhenAvailable>true</StartWhenAvailable>
        <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
        <IdleSettings>
          <Duration>PT10M</Duration>
          <WaitTimeout>PT1H</WaitTimeout>
          <StopOnIdleEnd>true</StopOnIdleEnd>
          <RestartOnIdle>false</RestartOnIdle>
        </IdleSettings>
        <AllowStartOnDemand>true</AllowStartOnDemand>
        <Enabled>true</Enabled>
        <Hidden>false</Hidden>
        <RunOnlyIfIdle>false</RunOnlyIfIdle>
        <WakeToRun>false</WakeToRun>
        <ExecutionTimeLimit>PT72H</ExecutionTimeLimit>
        <Priority>7</Priority>
      </Settings>
      <Actions Context="Author">
        <Exec>
          <Command>{3}</Command>
          <Arguments>{4}</Arguments>
        </Exec>
      </Actions>
    </Task>'''
    if is_frozen():
        with open(path + r"\data\startup.xml", "w") as file:
            file.write(xml.format("LazyGamer", time, "".join(map(lambda x: days_list[x], days.split(","))),
                                  f"{path}\\LazyGamer.exe", "--silent"))
        subprocess.Popen(
            ['schtasks.exe', '/create', '/TN', "LazyGamer", "/xml", fr'{PATH}\data\startup.xml'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        pythonw_path = get_path_pythonw()
        main_path = path + "\\main.py"
        command = fr'''"{main_path}" --silent'''
        with open(path + r"\data\startup.xml", "w") as file:
            file.write(
                xml.format("LazyGamer", time, "".join(map(lambda x: days_list[x], days.split(","))), pythonw_path,
                           command))
        subprocess.Popen(
            ['schtasks.exe', '/create', '/TN', "LazyGamerPy", "/xml", fr'{PATH}\data\startup.xml'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


def disable_startup():
    subprocess.Popen(['schtasks.exe', '/delete', '/TN', "LazyGamer", "/F"], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    subprocess.Popen(['schtasks.exe', '/delete', '/TN', "LazyGamerPy", "/F"], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


def raise_console(console_toggle):
    """Brings up the Console Window."""
    if console_toggle:
        # Show console
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)
    else:
        # Hide console
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


if __name__ == "__main__":
    create_config()
else:
    remove_old_options()
    set_new_options()
