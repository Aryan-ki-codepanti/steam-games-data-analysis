import requests
import json
import csv


def fetch_current_players(app_id):
    # parse int to str
    app_id = str(app_id) if isinstance(app_id, int) else app_id

    try:
        response_API = requests.get(
            f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid={app_id}')
        if response_API.status_code == 200:
            data = response_API.text
            parse_json = json.loads(data)
            return parse_json['response']['player_count']
        return "null"

    except Exception as e:
        print(f"Exception (FETCH_CURRENT_PLAYERS) at {app_id} , \n{e}")
        return "null"

# 25s -> 50reqs


def main():
    with open("data/games.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        rec = next(reader)
        for i in range(4):
            id = rec[0]
            print(id, fetch_current_players(id))

            rec = next(reader)


if __name__ == "__main__":
    main()
    print(fetch_current_players(730))
