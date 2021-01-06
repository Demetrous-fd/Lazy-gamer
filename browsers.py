import json
import webbrowser
from os import getenv
from time import sleep
from config import AUTH_URL
from selenium import webdriver
from scrapy import get_remote_link
from os.path import exists, getsize
from fake_useragent import UserAgent
from msedge.selenium_tools import Edge
from selenium.webdriver.common.by import By
from msedge.selenium_tools import EdgeOptions
from settings import update_setting, get_setting
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def write_game(game):
    games = [{"game": game}]
    if exists(r"data\left game.json") and getsize(r"data\left game.json") > 0:
        with open(r"data\left game.json") as file:
            temp = json.load(file)

        for game in temp:
            games.append({"game": game["game"]})

    with open(r"data\left game.json", "w") as file:
        json.dump(games, file, indent=4)


def select_browser(name, headless=False, remote=False):
    useragent = UserAgent()
    if name == "chrome":
        chromeoptions = webdriver.ChromeOptions()
        chromeoptions.add_argument("--window-size=1920,1080")
        chromeoptions.add_argument("start-maximized")
        chromeoptions.add_argument("--enable-profile-shortcut-manager")
        chromeoptions.add_argument("--allow-profiles-outside-user-dir")
        chromeoptions.add_argument(
            "user-data-dir=" + "\\".join(
                getenv("appdata").split("\\")[0:-1]) + r"\Local\Google\Chrome\User Data\Profile 2")
        chromeoptions.add_argument("--profile-directory=Default")
        chromeoptions.add_argument(f"user-agent={useragent.chrome}")

        if remote:
            chromeoptions.add_argument("--remote-debugging-port=9222")

        if headless:
            chromeoptions.add_argument("headless")
            chromeoptions.add_argument("--disable-gpu")
            return webdriver.Chrome(ChromeDriverManager().install(),
                                    chrome_options=chromeoptions)
        else:
            return webdriver.Chrome(ChromeDriverManager().install(),
                                    chrome_options=chromeoptions)

    elif name == "edge":
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("--allow-profiles-outside-user-dir")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")
        options.add_argument("user-data-dir=" + "\\".join(
            getenv("appdata").split("\\")[0:-1]) + r"\Local\Microsoft\Edge\User Data\Profile 2")
        options.add_argument("--profile-directory=Default")
        options.add_argument(f"user-agent={useragent.edge}")

        if remote:
            options.add_argument("--remote-debugging-port=9222")

        if headless:
            options.add_argument("headless")
            return Edge(EdgeChromiumDriverManager().install(), options=options)
        else:
            return Edge(EdgeChromiumDriverManager().install(), options=options)


class Browser:

    def __init__(self, name_browser=get_setting("Settings", "browser")):
        self.__browser = name_browser

    def launch_browser(self, url="https://www.epicgames.com", headless=False, remote=False):
        """
        The launch browser and open site.

        :param url: Link to the site.
        :type url: str
        :param headless: The hide browser.
        :type headless: bool
        :param remote: Activate remote panel
        :type remote: bool
        """

        print("Launch browser")
        if headless and remote:
            self.__driver = select_browser(self.__browser, True, True)
            print("Remote panel: " + get_remote_link(self.__browser))
        elif headless:
            self.__driver = select_browser(self.__browser, True)
        else:
            self.__driver = select_browser(self.__browser)

        self.__driver.get(url)

    def login(self):
        self.launch_browser(AUTH_URL, True, True)
        print("Через пару секунд откроется окно авторизации")
        sleep(3)
        webbrowser.open_new(get_remote_link(self.__browser))
        while True:
            try:
                WebDriverWait(self.__driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.focusable.is-logged-in.text-color-hover"))
                )
                break
            except Exception:
                continue
        sleep(3)
        self.quit()
        update_setting("Settings", "auth", "True")
        print("Авторизация прошла успешно!")
        print("-" * 50)

    def check_login(self):
        if self.__driver.current_url == "https://www.epicgames.com/id/logout?lang=ru&redirectUrl=https%3A%2F%2Fwww.epicgames.com" \
                or self.__driver.current_url == "https://www.epicgames.com/id/login?lang=ru&noHostRedirect=true&redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fstore%2F&client_id=875a3b57d3a640a6b7f9b4e883463ab4":
            update_setting("Settings", "auth", "False")
            return True
        try:
            WebDriverWait(self.__driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, """//*[@id="user"]"""))
            )
        finally:
            sleep(5)
            if self.__driver.find_element_by_xpath("""//*[@id="user"]/ul/li/a/span""").text.lower() == "вход":
                self.__driver.quit()
                print("Слетела авторизация\nАвторизуйтесь заново")
                print("-" * 50)
                update_setting("Settings", "auth", "False")
                sleep(3)
                return True
            else:
                return False

    def __add_game(self, game):
        try:
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            """//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div/div/div[3]/div/div/button"""))
            )
        finally:
            self.__driver.find_element_by_xpath(
                """//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div/div/div[3]/div/div/button""").click()
        try:
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            """//*[@id="purchase-app"]/div/div[4]/div[1]/div[2]/div[5]/div/div/button"""))
            )
        finally:
            self.__driver.find_element_by_xpath(
                """//*[@id="purchase-app"]/div/div[4]/div[1]/div[2]/div[5]/div/div/button""").click()
        write_game(game)
        print(f"{game} добавлена в коллекцию")

    def __choices(self, game, button_text):
        if button_text == "купить сейчас":
            print("Игра платная")
        elif button_text == "в коллекции":
            write_game(game)
            print(f"{game} имеется в библиотеке")
        elif button_text == "получить":
            self.__add_game(game)
        else:
            pass

    def get_free_game(self, game, url):
        self.__driver.get(url)
        self.__driver.implicitly_wait(10)
        print(self.__driver.current_url)
        if self.check_login():
            self.login()
            self.launch_browser(url, True)
            self.get_free_game(game, url)

        try:
            WebDriverWait(self.__driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-a8mpwg-WarningLayout__contentWrapper"))
            )
        except TimeoutException:
            pass
        finally:
            try:
                if self.__driver.find_element_by_css_selector("div.css-a8mpwg-WarningLayout__contentWrapper"):
                    print("18+")
                    self.__driver.find_element_by_css_selector("button.css-19tmzba").click()
            except NoSuchElementException:
                print("Not 18+")
        try:
            if self.__driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div[4]/main/div/div[3]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div/a"):  # Дополнительные предложения
                button_text = self.__driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div[4]/main/div/div[3]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div/button").text.lower()
                self.__choices(game, button_text)

        except NoSuchElementException:  # Нет дополнительных предложений
            try:
                WebDriverWait(self.__driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-1tv9h97"))
                )
            except TimeoutException:
                pass
            finally:
                button_text = self.__driver.find_element_by_css_selector("div.css-1tv9h97").text.lower()
                self.__choices(game, button_text)

    def get_screenshot(self, name):
        if name.split(".")[-1] != "png" or "." not in name:
            name = name.split(".")[0] + ".png"
        self.__driver.get_screenshot_as_file(name)

    def quit(self):
        self.__driver.quit()
        print("Close browser")
