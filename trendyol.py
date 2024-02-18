import requests
import time
from bs4 import BeautifulSoup
import json


def extract_categories(categories):
    extracted_categories = {}
    for category in categories:
        category_title = category["title"]
        extracted_categories[category_title] = {}
        children = category.get("children", [])
        if children:
            extracted_categories[category_title] = extract_categories(children)
        else:
            extracted_categories[category_title] = {
                "webUrl": category.get("webUrl", ""),
            }
    return extracted_categories


status_code = 0
url = "https://www.trendyol.com/en"
while status_code != 200:
    response = requests.get(url, timeout=5)
    status_code = response.status_code
    if status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        script_tags = soup.find_all("script")
        for script in script_tags:
            if script.string and "__header__PROPS" in script.string:
                script_content = script.string
                json_data_string = script_content.replace(
                    'window["__header__PROPS"]=', ""
                )
                json_data = json.loads(json_data_string)

                categories = json_data.get("categories", [])
                main_categories = extract_categories(categories)

                with open("categories.json", "w") as json_file:
                    json.dump(main_categories, json_file, indent=4)

                break

    time.sleep(5)
