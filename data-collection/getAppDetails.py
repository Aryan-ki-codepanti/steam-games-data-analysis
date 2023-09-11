from utils import EMPTY_VALUE, parse__requirements_html
import requests
import json
import csv

# development
from pprint import pprint


def fetch_app_details(app_id):

    app_id = str(app_id) if isinstance(app_id, int) else app_id

    try:
        response_API = requests.get(
            f'https://store.steampowered.com/api/appdetails?appids={app_id}&cc=91')
        if response_API.status_code == 200:
            data = response_API.text
            app_details = json.loads(data)[app_id]

            # check valid response
            if not app_details["success"]:
                return EMPTY_VALUE

            app_details = app_details["data"]

            '''
                Title - done 
                Price - done
                Developer - done
                Publisher - done
                Genre - done 
                Tags (categories) - done
                PEGI rating (required_age) - done
                Achievements number - done
                Release date - done
                Metacritic rating - done
                Requirements-


                - dlc : boolean if there is any downloadable content - done
                Support - done
                - win
                - linux
                - mac 
            '''

            title = EMPTY_VALUE if "name" not in app_details else app_details["name"]

            initial_price = EMPTY_VALUE if "price_overview" not in app_details or "initial" not in app_details[
                "price_overview"] else app_details["price_overview"]["initial"]/100
            final_price = EMPTY_VALUE if "price_overview" not in app_details or "final" not in app_details[
                "price_overview"] else app_details["price_overview"]["final"]/100
            discount_percent = EMPTY_VALUE if "price_overview" not in app_details or "discount_percent" not in app_details[
                "price_overview"] else app_details["price_overview"]["discount_percent"]

            # set 0 if free
            if "is_free" in app_details and app_details["is_free"]:
                initial_price = final_price = discount_percent = 0

            developers = EMPTY_VALUE if "developers" not in app_details else app_details[
                "developers"]

            publishers = EMPTY_VALUE if "publishers" not in app_details else app_details[
                "publishers"]

            genres = EMPTY_VALUE if "genres" not in app_details else [
                x["description"] for x in app_details["genres"]]

            categories = EMPTY_VALUE if "categories" not in app_details else [
                x["description"] for x in app_details["categories"]]

            required_age = 0 if "required_age" not in app_details else app_details[
                "required_age"]

            achievements = EMPTY_VALUE if "achievements" not in app_details or "total" not in app_details[
                "achievements"] else app_details["achievements"]["total"]

            release_date = EMPTY_VALUE if "release_date" not in app_details or "date" not in app_details[
                "release_date"] else app_details["release_date"]["date"]

            metacritic_score = EMPTY_VALUE if "metacritic" not in app_details or "score" not in app_details["metacritic"] else app_details[
                "metacritic"]["score"]

            dlc_flag = "dlc" in app_details

            win_flag = mac_flag = linux_flag = EMPTY_VALUE

            if "platforms" in app_details:
                win_flag = app_details["platforms"].get("windows", EMPTY_VALUE)
                mac_flag = app_details["platforms"].get("mac", EMPTY_VALUE)
                linux_flag = app_details["platforms"].get("linux", EMPTY_VALUE)

            pc_requirements_html = EMPTY_VALUE if "pc_requirements" not in app_details or "minimum" not in app_details[
                "pc_requirements"] else app_details["pc_requirements"]["minimum"]

            pc_requirements = parse__requirements_html(pc_requirements_html)

            # os, processor , memory , graphics , directX , storage
            return [title, initial_price, final_price, discount_percent, developers, publishers, genres, categories, required_age, achievements, release_date, metacritic_score, dlc_flag, win_flag, mac_flag, linux_flag] + pc_requirements

        return EMPTY_VALUE
    except Exception as e:
        print(f"Exception at {e}")
        return EMPTY_VALUE

# 25s -> 50reqs


def main(n=1):
    with open("data/games.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        rec = next(reader)
        for i in range(n):
            id = rec[0]
            print(id)
            pprint(fetch_app_details(id))
            fetch_app_details(id)
            print('\n\n\n')

            rec = next(reader)


if __name__ == "__main__":
    main(6)
    pprint(fetch_app_details(app_id=730))
    pprint(fetch_app_details(app_id=1097880))

