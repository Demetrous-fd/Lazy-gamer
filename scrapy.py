import os
import sys
import json
import ctypes
import winreg
import requests
from time import sleep
from config import PROMO_URL
from functools import lru_cache
from fake_useragent import UserAgent
from os.path import abspath, dirname
from inspect import getframeinfo, currentframe

URL = PROMO_URL

useragent = {'User-Agent': UserAgent().random}
temp_list = []


def path():
    if is_frozen():
        return os.path.dirname(sys.executable)
    else:
        filename = getframeinfo(currentframe()).filename
        return dirname(abspath(filename))


def get_info():
    response = requests.get(URL, headers=useragent)
    if response.status_code == 200:
        data = json.loads(response.text)

        for item in data["data"]["Catalog"]["searchStore"]["elements"]:
            temp_list.append({
                "game": item["title"],
                "link": "https://www.epicgames.com/store/ru/product/" + item["productSlug"],
                "productSlug": item["productSlug"],
                "promo": item["promotions"]
            })

        with open(path() + r"\data\last_game.json", "w") as file:
            json.dump(temp_list, file, indent=4)
    else:
        print("EGS недоступен")
        print("Статус" + str(response.status_code))


@lru_cache(3)
def response_egs_api(product_slug: str):
    if "/" in product_slug:
        product_slug = product_slug.split("/")[0]
    return requests.get(f"https://store-content.ak.epicgames.com/api/ru/content/products/{product_slug}").json()


def get_age_gate(product_slug: str):
    r = response_egs_api(product_slug)
    return r["pages"][0]["ageGate"]["hasAgeGate"]


def list_offers(product_slug: str):
    r = response_egs_api(product_slug)
    if len(r["pages"]) > 1:
        return True
    else:
        return False


def get_remote_link(browser):
    for i in range(3):
        try:
            data = json.loads(requests.get("http://localhost:9222/json/list").text)
            dev = data[0]["devtoolsFrontendUrl"][9:]

            data = json.loads(requests.get("http://localhost:9222/json/version").text)
            ver = data["WebKit-Version"].split(" ")[1][1:-1]

            if browser == "chrome":
                return "https://chrome-devtools-frontend.appspot.com/serve_file/" + ver + dev + "&remoteFrontend=true"
            elif browser == "edge":
                return "https://devtools.azureedge.net/serve_file/" + ver + dev
            else:
                return
        except Exception:
            sleep(i)


def is_frozen():
    if getattr(sys, 'frozen', False):
        return True
    else:
        return False


def is_console():
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    process_array = (ctypes.c_uint * 1)()
    num_processes = kernel32.GetConsoleProcessList(process_array, 1)
    if num_processes == 2:  # Console
        return True
    else:  # Executable
        return False


def get_path_pythonw():
    if sys.version_info.minor == 8:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Python\PythonCore\3.8\InstallPath", 0,
                            winreg.KEY_READ) as key:
            return winreg.QueryValueEx(key, "WindowedExecutablePath")[0]
    elif sys.version_info.minor == 9:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Python\PythonCore\3.9\InstallPath", 0,
                            winreg.KEY_READ) as key:
            return winreg.QueryValueEx(key, "WindowedExecutablePath")[0]
    elif sys.version_info.minor == 7:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Python\PythonCore\3.7\InstallPath", 0,
                            winreg.KEY_READ) as key:
            return winreg.QueryValueEx(key, "WindowedExecutablePath")[0]


if __name__ == '__main__':
    get_info()