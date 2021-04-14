import os
import winreg
import logging
import requests
from functools import lru_cache
from win32api import GetFileVersionInfo, LOWORD, HIWORD

from webdriver_manager import utils
from webdriver_manager.driver import Driver
from webdriver_manager.logger import log
from webdriver_manager.manager import DriverManager
from webdriver_manager.utils import ChromeType, validate_response, OSType, os_name, download_file


@lru_cache(1)
def get_installed_browsers() -> dict:
    browsers = dict()
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Clients\StartMenuInternet", 0, winreg.KEY_READ) as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            browser = winreg.EnumKey(key, i)
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                fr"SOFTWARE\WOW6432Node\Clients\StartMenuInternet\{browser}\shell\open", 0,
                                winreg.KEY_READ) as key1:
                browsers[browser] = winreg.QueryValue(key1, "command")

    for name in browsers:
        browsers[name] = browsers[name].replace('"', "")

    return browsers


def get_version(path: str) -> str:
    try:
        info = GetFileVersionInfo(path, "\\")
        ms: str = info['FileVersionMS']
        ls: str = info['FileVersionLS']
        return f"{HIWORD(ms)}.{LOWORD(ms)}.{HIWORD(ls)}.{LOWORD(ls)}"
    except Exception as ex:
        print(ex)
        return "Unknown version"


def browser_exists(browser: str) -> bool:
    return True if browser in get_installed_browsers() else False


def browser_version(browser: str):
    return get_version(get_installed_browsers()[browser])


class ChromeDriver(Driver):
    def __init__(self, name, version, os_type, url, latest_release_url,
                 chrome_type=ChromeType.GOOGLE):
        super(ChromeDriver, self).__init__(name, version, os_type, url,
                                           latest_release_url)
        self.chrome_type = chrome_type
        self.browser_version = ".".join(browser_version("Google Chrome").split(".")[:-1])

    def get_os_type(self):
        if "win" in super().get_os_type():
            return "win32"
        return super().get_os_type()

    def get_latest_release_version(self):
        log(f"Get LATEST driver version for {self.browser_version}")
        resp = requests.get(f"{self._latest_release_url}_{self.browser_version}")
        validate_response(resp)
        return resp.text.rstrip()


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="chromedriver",
                 url="https://chromedriver.storage.googleapis.com",
                 latest_release_url="https://chromedriver.storage.googleapis.com/LATEST_RELEASE",
                 chrome_type=ChromeType.GOOGLE,
                 log_level=logging.INFO,
                 print_first_line=True,
                 cache_valid_range=1):
        super().__init__(path, log_level=log_level, print_first_line=print_first_line,
                         cache_valid_range=cache_valid_range)

        self.driver = ChromeDriver(name=name,
                                   version=version,
                                   os_type=os_type,
                                   url=url,
                                   latest_release_url=latest_release_url,
                                   chrome_type=chrome_type)

    def install(self):
        log(f"Current {self.driver.chrome_type} version is {self.driver.browser_version}", first_line=True)
        driver_path = self._get_driver_path(self.driver)

        os.chmod(driver_path, 0o755)
        return driver_path


class EdgeChromiumDriver(Driver):
    def __init__(self, name, version, os_type, url, latest_release_url):
        super(EdgeChromiumDriver, self).__init__(name, version, os_type, url,
                                                 latest_release_url)
        self.browser_version = ""

    def get_latest_release_version(self):
        # type: () -> str
        if os_name() == OSType.LINUX:
            latest_release_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
        else:
            major_edge_version = browser_version("Microsoft Edge").split(".")[0]
            latest_release_url = self._latest_release_url + '_' + major_edge_version
        resp = requests.get(latest_release_url)
        validate_response(resp)
        return resp.text.rstrip()


class EdgeChromiumDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="edgedriver",
                 url="https://msedgedriver.azureedge.net",
                 latest_release_url="https://msedgedriver.azureedge.net/"
                                    "LATEST_RELEASE",
                 log_level=None,
                 print_first_line=None,
                 cache_valid_range=1):
        super().__init__(path, log_level, print_first_line, cache_valid_range)
        self.driver = EdgeChromiumDriver(version=version,
                                         os_type=os_type,
                                         name=name,
                                         url=url,
                                         latest_release_url=latest_release_url)

    def install(self):
        return self._get_driver_path(self.driver)


if __name__ == '__main__':
    print(get_installed_browsers())
    print("Google Chrome", browser_exists("Google Chrome"), browser_version("Google Chrome"))
    print("Microsoft Edge", browser_exists("Microsoft Edge"), browser_version("Microsoft Edge"))
