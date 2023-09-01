import csv,bs4,requests

session = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64;6 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
 
def scrape(app_id):
        link = "https://store.steampowered.com/app/"+app_id
        res = session.get(link,headers = headers)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text,'html.parser')
        elem1 = soup.select('#genresAndManufacturer')
        return elem1[0].text.strip()           
   
pass


def main():
    with open("data/app_ids.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        rec = next(reader, False)
        rec = next(reader, False)

        # required to do
        # while rec:

        # testing purpose : 50 ids
        for i in range(50):
            app_id = rec[0]
            # scrape for app_id
            # scrape(app_id)
            rec = next(reader, False)
            print(scrape(app_id))


main()
