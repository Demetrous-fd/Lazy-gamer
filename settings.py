from scrapy import path, is_frozen, get_path_pythonw
from os.path import exists
from os import mkdir
import configparser
import subprocess
import winreg
import ctypes


PATH = path() + "\\data\\settings.ini"


def create_config():
    if not exists(path() + "\\data"):
        mkdir(path() + "\\data")

    config = configparser.ConfigParser()

    config.add_section("Settings")
    config.set("Settings", "browser", "chrome")
    config.set("Settings", "auth", "False")

    config.add_section("StartUp")
    config.set("StartUp", "everyday", "False")
    config.set("StartUp", "sometimes", "False")
    config.set("StartUp", "days", "NULL")
    config.set("StartUp", "time", "NULL")

    config.add_section("WebDriver")
    config.set("WebDriver", "driver_manager", "True")
    config.set("WebDriver", "chrome_driver_path", "NULL")
    config.set("WebDriver", "msedge_driver_path", "NULL")

    config.add_section("Other")
    config.set("Other", "last_launch", "")

    with open(PATH, "w") as config_file:
        config.write(config_file)


def get_config():
    if not exists(PATH):
        create_config()

    config = configparser.ConfigParser()
    config.read(PATH)
    return config


def get_setting(section, setting):
    config = get_config()
    value = config.get(section, setting)
    return value


def update_setting(section, setting, value):
    config = get_config()
    config.set(section, setting, value)
    with open(PATH, "w") as config_file:
        config.write(config_file)


def enable_startup(everyday=True):
    path = PATH
    if not is_frozen():
        pythonw_path = get_path_pythonw()
    if everyday:
        if is_frozen():
            path += "\\LazyGamer.exe"
            command = f'"{path}" --silent'

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                winreg.KEY_WRITE) as key:

                winreg.SetValueEx(key, "LazyGamer", 0, winreg.REG_SZ, command)

        else:
            path += "\\main.py"
            command = f'''"{pythonw_path}" "{path}" --silent'''
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "LazyGamerPy", 0, winreg.REG_SZ, command)
    else:
        days = get_setting("StartUp", "days")
        time = get_setting("StartUp", "time")
        if is_frozen():
            path += "\\LazyGamer.exe"
            command = fr'"{path}" --silent'
            up = subprocess.Popen(
                ['schtasks.exe', '/create', '/TN', "LazyGamer", "/tr", command, "/SC", "weekly", "/d", days,
                 "/st", time], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            path += "\\main.py"
            command = fr'''"{pythonw_path}" "{path}" --silent'''
            subprocess.Popen(
                ['schtasks.exe', '/create', '/TN', "LazyGamerPy", "/tr", command, "/SC", "weekly", "/d", days,
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