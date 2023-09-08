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
    release_date = soup.select_one('#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div.release_date > div.date')
    
    language_table = soup.find('div', {'id': 'languageTable'})
    language_rows = language_table.find_all('tr')

    lang = []

    for row in language_rows:
        language_name = row.find('td', {'class': 'ellipsis'})
        if language_name:
            lang.append(language_name.get_text(strip=True))

    p_review = soup.select_one('#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(5) > span')
    n_review = soup.select_one('#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(8) > span')
    t_review = soup.select_one('#review_histogram_rollup_section > div.user_reviews_summary_bar > div > span:nth-child(3)')
    ov_review = soup.select_one('#review_histogram_rollup_section > div.user_reviews_summary_bar > div > span.game_review_summary.positive')
    m_content = soup.select_one('#game_area_content_descriptors > p:nth-child(3)')
    
    return[release_date, lang, p_review, n_review, t_review, ov_review, m_content]

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
