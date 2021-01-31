import configparser
from os.path import exists, abspath, dirname
from inspect import getframeinfo, currentframe

filename = getframeinfo(currentframe()).filename
workpath = dirname(abspath(filename))
PATH = workpath + "\\settings.ini"


def create_config():
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "browser", "chrome")
    config.set("Settings", "path", workpath)
    config.set("Settings", "auth", "False")
    config.add_section("StartUp")
    config.set("StartUp", "everyday", "False")
    config.set("StartUp", "sometimes", "False")
    config.set("StartUp", "days", "NULL")
    config.set("StartUp", "time", "NULL")
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


if __name__ == "__main__":
    create_config()