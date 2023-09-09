import requests
import json
import csv


def fetch_users(app_id):
    # response_API = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid={app_id}')

    try:
        response_API = requests.get(
            f'https://store.steampowered.com/api/appdetails?appids={app_id}&cc=91')
        if response_API.status_code == 200:
            data = response_API.text
            parse_json = json.loads(data)

            # return parse_json['response']['player_count']
            return parse_json
    except Exception as e:
        print(f"Exception at {e}")
        return "null"

# 25s -> 50reqs


def main():
    with open("games.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        rec = next(reader)
        for i in range(1):
            id = rec[0]
            print(id, fetch_users(id))

            rec = next(reader)


if __name__ == "__main__":
    main()
