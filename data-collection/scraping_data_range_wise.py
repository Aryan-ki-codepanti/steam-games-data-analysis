from utils import EMPTY_VALUE
import csv
import bs4
import requests

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64;6 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

EMPTY_ARRAY = [EMPTY_VALUE] * 12
EMPTY_ARRAY[0:3] = ['English']*3

def scrape(app_id):
    # parse int to str
    app_id = str(app_id) if isinstance(app_id, int) else app_id

    link = "https://store.steampowered.com/app/"+app_id
    res = session.get(link, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    language_table = soup.find('div', {'id': 'languageTable'})

    # three category support
    lang__interface = []
    lang__full_audio = []
    lang__subtitles = []

    # handle when language table is none
    language_rows = [] if language_table is None else language_table.find_all('tr')

    for row in language_rows:
        language_name = row.find('td', {'class': 'ellipsis'})

        if language_name:
            lang_name = language_name.get_text(strip=True)
            support_type = row.find_all('td', {'class': 'checkcol'})

            # extra check
            if support_type and len(support_type) == 3:
                if support_type[0].get_text(strip=True):
                    lang__interface.append(lang_name)
                if support_type[1].get_text(strip=True):
                    lang__full_audio.append(lang_name)
                if support_type[2].get_text(strip=True):
                    lang__subtitles.append(lang_name)

    # default english
    lang__interface = ["English"] if not lang__interface else lang__interface
    lang__full_audio = [
        "English"] if not lang__full_audio else lang__full_audio
    lang__subtitles = ["English"] if not lang__subtitles else lang__subtitles

    positive_reviews = soup.select_one(
        '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(5) > span')
    negative_reviews = soup.select_one(
        '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(8) > span')
    total_reviews = soup.select_one(
        '#review_histogram_rollup_section > div.user_reviews_summary_bar > div > span:nth-child(3)')
    overall_review_summary = soup.select_one(
        '#review_histogram_rollup_section > div.user_reviews_summary_bar > div > span.game_review_summary')
    m_content = soup.select_one(
        '#game_area_content_descriptors > p:nth-child(3)')
    award = soup.select_one(
        '.steamawards2020_app_banner_header.award_title.small')
    curator = soup.select_one(
        '.no_curators_followed'
    )
    recent_review_summary = soup.select_one(
        '#review_histogram_recent_section > div.user_reviews_summary_bar > div'
    )
    recent_review_count = soup.select_one(
        '#review_histogram_recent_section > div.user_reviews_summary_bar > div > span:nth-child(3)'
    )
    # Parsing text and adding checks to avoid  errors for None.<property_access>[()]
    positive_reviews = EMPTY_VALUE if positive_reviews is None else positive_reviews.get_text(strip=True)[
        1:-1]
    negative_reviews = EMPTY_VALUE if negative_reviews is None else negative_reviews.get_text(strip=True)[
        1:-1]
    total_reviews = EMPTY_VALUE if total_reviews is None else total_reviews.get_text(strip=True)[
        1:-1].split()[0]
    overall_review_summary = EMPTY_VALUE if overall_review_summary is None else overall_review_summary.get_text(strip=True)
    m_content = EMPTY_VALUE if m_content is None else m_content.get_text(strip=True)
    award = EMPTY_VALUE if award is None else award.get_text(strip=True)
    curator = EMPTY_VALUE if curator is None else curator.get_text(strip=True).strip()[0]

    # recent review parsing
    recent_review_list = None if recent_review_summary is None else recent_review_summary.get_text(strip=True).strip()[
        16:].split('\n')
    recent_review_summary = EMPTY_VALUE if recent_review_list is None or not recent_review_list[
        0] else recent_review_list[0]
    recent_review_count = EMPTY_VALUE if recent_review_list is None or not recent_review_list[
        0] else recent_review_list[1][1:-1].split()[0]

    return [lang__interface, lang__full_audio, lang__subtitles, positive_reviews, negative_reviews, total_reviews, overall_review_summary,recent_review_count ,recent_review_summary ,m_content, award, curator]


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


if __name__ == "__main__":
    # main()
    # main(0, 2)
    main(1000, 1004)
    # print(scrape(730))
