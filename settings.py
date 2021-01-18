import configparser
from os.path import exists, abspath

PATH = "\\".join(abspath(__file__).split("\\")[0:-1]) + "\\settings.ini"


def create_config():
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "browser", "chrome")
    config.set("Settings", "startup", "False")
    config.set("Settings", "path", "\\".join(abspath(__file__).split("\\")[0:-1]))
    config.set("Settings", "auth", "False")
    print(PATH)

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
