import csv
import bs4
import requests

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64;6 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}


def scrape(app_id):
    link = "https://store.steampowered.com/app/"+app_id
    res = session.get(link, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elem1 = soup.select('#genresAndManufacturer')
    return elem1[0].text.strip()


pass


# inclusive both , 0 based
# min : 0
# max : 76986
def main(start=0, end=0):
    with open("data/app_ids.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        rec = next(reader, False)
        rec = next(reader, False)

        app_ids = []

        # required to do
        while rec:
            app_ids.append(rec[0])
            rec = next(reader, False)

        # testing purpose : 50 ids
        for i in range(start, end + 1):
            app_id = app_ids[i]
            # scrape for app_id
            # scrape(app_id)
            try:
                print(scrape(app_id))
            except Exception as e:
                print(f"ERROR at : {app_id}")
                print(e)

            finally:
                rec = next(reader, False)


# main()
main(10, 20)
