import csv
import bs4
import requests

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64;6 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}



def getIds(url: str, save_file_name):

    res = session.get(url, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')


    limit = soup.select_one("#body > div:nth-child(1) > p:nth-child(3)").get_text(strip=True).split()[1]
    print(limit)

    
    with open(f"data/{save_file_name}.csv", "w") as f:
        for i in range(1, int(limit) + 1):
            game_box = soup.find('div',  {'id': i})
            span = game_box.find('span', {'class': 'title'})
            game_link = span.find('a')
            id_ = game_link.attrs['href'].split('/')[-1]
            print(id_)
            f.write(f"{id_}\n")


if __name__ == "__main__":

    # getIds("https://steam250.com/top250", "steam250_top_50")
    # getIds("https://steam250.com/hidden_gems", "steam250_hidden_gems")
    # getIds("https://steam250.com/most_played", "steam250_most_played" )
    
    getIds("https://steam250.com/old", "steam250_pre2006" )

    for i in range(2007,2024):
        getIds(f"https://steam250.com/{i}", f"steam250_bestOf{i}" )

