import subprocess
from os import environ
"""wmic datafile where "name='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'" get version"""
"""wmic datafile where "name='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'" get version"""
f"""wmic datafile where "name='{environ['LOCALAPPDATA']}\\Yandex\\YandexBrowser\\Application\\browser.exe'" get version"""


"""https://github.com/yandex/YandexDriver/releases"""
"""https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"""
"""https://sites.google.com/a/chromium.org/chromedriver/downloads"""

"""https://github.com/mozilla/geckodriver/releases"""


def get_version_browser(browser=""):
    spath = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    cargs = ["wmic", "datafile", "where"]
    process = subprocess.check_output(cargs)
    # result = subprocess.run(['wmic', r"""datafile where "name='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'" get version"""], stdout=subprocess.PIPE, encoding='cp866')
    # return result.stdout
    print(process.strip().decode("cp866"))


# print(get_version_browser(2))
get_version_browser()
