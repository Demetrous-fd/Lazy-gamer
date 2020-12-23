import json
import pickle
from time import sleep
from config import AUTH_URL
from random import randrange
from selenium import webdriver
from os.path import exists, getsize
from fake_useragent import UserAgent
from msedge.selenium_tools import Edge
from selenium.webdriver.common.by import By
from msedge.selenium_tools import EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def select_browser(name, headless=False):
    useragent = UserAgent()
    if name == "chrome":
        chromeoptions = webdriver.ChromeOptions()
        chromeoptions.add_argument(f"user-agent={useragent.chrome}")
        if headless:
            chromeoptions.add_argument("headless")
            return webdriver.Chrome(executable_path=r"data\drivers\chromedrivers\chromedriver86.exe",
                                    chrome_options=chromeoptions)
        else:
            return webdriver.Chrome(executable_path=r"data\drivers\chromedrivers\chromedriver86.exe",
                                    chrome_options=chromeoptions)

    elif name == "yandex":
        chromeoptions = webdriver.ChromeOptions()
        chromeoptions.add_argument(f"user-agent={useragent.chrome}")
        if headless:
            chromeoptions.add_argument("headless")
            return webdriver.Chrome(executable_path=r"data\drivers\yandexdriver.exe", chrome_options=chromeoptions)
        else:
            return webdriver.Chrome(executable_path=r"data\drivers\yandexdriver.exe", chrome_options=chromeoptions)

    elif name == "edge":
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-agent={useragent.edge}")
        if headless:
            options.add_argument("headless")
            options.add_argument("disable-gpu")
            return Edge(executable_path=r"data\drivers\msedgedriver87_666.exe", options=options)
        else:
            return Edge(executable_path=r"data\drivers\msedgedriver87_666.exe", options=options)

    elif name == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("general.useragent.override", useragent.ff)
        if headless:
            options.headless = True
            return webdriver.Firefox(executable_path=r"data\drivers\geckodriver.exe", options=options)
        else:
            return webdriver.Firefox(executable_path=r"data\drivers\geckodriver.exe", options=options)


class Browser:

    def __init__(self, name_browser):
        self.__browser = name_browser

    def launch_browser(self, url="https://www.epicgames.com", headless=False):
        """
        The launch browser and open site.

        :param url: Link to the site.
        :type url: str
        :param headless: The hide browser.
        :type headless: bool
        """

        print("Launch browser")
        if headless:
            self.__driver = select_browser(self.__browser, True)
        else:
            self.__driver = select_browser(self.__browser)

        self.__driver.get(url)

        if exists("data/cookies.pkl"):
            self.__session()
            self.__driver.refresh()

    def __session(self, save=False):
        if save:
            with open("data/cookies.pkl", "wb") as file:
                pickle.dump(self.__driver.get_cookies(), file)
            print("Save cookies")

        else:
            cookies = pickle.load(open("data/cookies.pkl", "rb"))
            print("Load cookies")
            for cookie in cookies:
                self.__driver.add_cookie(cookie)

    def login(self):
        self.launch_browser(AUTH_URL)
        while True:
            try:
                WebDriverWait(self.__driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.focusable.is-logged-in.text-color-hover"))
                )
                break
            except Exception:
                continue
        self.__session(True)
        self.quit()
        print("Авторизация прошла успешно!")

    def check_login(self):
        if self.__driver.current_url == "https://www.epicgames.com/id/logout?lang=ru&redirectUrl=https%3A%2F%2Fwww.epicgames.com":
            print("Infinite Loop")
            self.quit()
        try:
            WebDriverWait(self.__driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, """//*[@id="user"]"""))
            )
        finally:
            print(self.__driver.current_url)
            if self.__driver.find_element_by_xpath("""//*[@id="user"]/ul/li/a/span""").text.lower() == "вход":
                self.__driver.quit()
                print("Слетела авторизация\nАвторизуйтесь заново")
                sleep(3)
                return True
            else:
                return False

    def get_free_game(self, game, url):
        self.__driver.get(url)
        if self.check_login():
            self.login()
            self.launch_browser(url, True)
            self.get_free_game(game, url)
        try:
            WebDriverWait(self.__driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-1tv9h97"))
            )
        except TimeoutException:
            pass
        finally:
            try:
                WebDriverWait(self.__driver, 10).until(
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
            if self.__driver.find_element_by_css_selector("div.css-1tv9h97").text.lower() == "в коллекции":
                write_game(game)
                print(f"{game} имеется в библиотеке")
                print("-" * 50)
            elif self.__driver.find_element_by_css_selector("div.css-1tv9h97").text.lower() == "купить сейчас":
                print("Игра платная")
            else:
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
                print("-" * 50)

    def get_screenshot(self, name):
        if name.split(".")[-1] != "png" or "." not in name:
            name = name.split(".")[0] + ".png"
        self.__driver.get_screenshot_as_file(name)

    def quit(self):
        self.__driver.quit()
        print("Close browser")
