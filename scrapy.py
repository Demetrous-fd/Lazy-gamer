import json
from os.path import exists

import requests
from config import PROMO_URL
from browsers import Browser
from fake_useragent import UserAgent

URL = PROMO_URL

useragent = {'User-Agent': UserAgent().random}
temp_list = []


# data = json.load(open("temp.json"))
# with open("test.json", "w") as file:
#     json.dump(data, file, indent=4)


def get_info():  # TODO: добавить обработку ответов запроса

    response = requests.get(URL, headers=useragent)
    data = json.loads(response.text)

    for item in data["data"]["Catalog"]["searchStore"]["elements"]:
        # print(item["title"])
        # print(item["keyImages"])
        # print("https://www.epicgames.com/store/ru/product/" + item["productSlug"])
        temp_list.append({
            "game": item["title"],
            "link": "https://www.epicgames.com/store/ru/product/" + item["productSlug"],
            "images": item["keyImages"]
        })

    with open("data/last_game.json", "w") as file:
        json.dump(temp_list, file, indent=4)
    with open("data/temp.json", "w") as file:
        json.dump(data, file, indent=4)


def get_users():
    if exists("data/acc.json"):
        return json.load(open("data/acc.json"))
    else:
        Browser("yandex").login()
        get_users()



if __name__ == '__main__':
    get_info()