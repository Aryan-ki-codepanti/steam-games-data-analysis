import csv
import bs4
import requests

from pprint import pprint

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64;6 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}


# returns list of new ids and last index of previous apps
def new_info(ids):

    # optimised lookup
    previous_ids = set()
    with open("data/apps.csv" , "r") as f:
        reader = csv.reader(f)
        next(reader)
        rec = next(reader, False)
        while rec:
            last_idx = rec[0]
            previous_ids.add(rec[1])
            rec = next(reader, False)
    
    # Filter new ids
    new_ids = [ id_ for id_ in  ids if id_ not in previous_ids ]

    return new_ids, last_idx

def getIds(url: str):

    res = session.get(url, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    limit = soup.select_one("#body > div:nth-child(1) > p:nth-child(3)").get_text(strip=True).split()[1]

    ids = []
    for i in range(1, int(limit) + 1):
        game_box = soup.find('div',  {'id': i})
        span = game_box.find('span', {'class': 'title'})
        game_link = span.find('a')
        id_ = game_link.attrs['href'].split('/')[-1]
        ids.append(id_)

    return ids

def runner(url : str):
    ids = getIds(url)
    ids, last_idx = new_info(ids)
    print(f"URL: {url}")
    print(f"New ids : {ids}")
    print(f"Count: {len(ids)}\n")

if __name__ == "__main__":

    urls = [
        "https://steam250.com/top250",
        "https://steam250.com/hidden_gems",
        "https://steam250.com/most_played",
        "https://steam250.com/old"
    ]

    for i in range(2007,2024):
        urls.append(f"https://steam250.com/{i}")


    for url in urls:
        runner(url)

    pass