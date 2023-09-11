from getCurrentPlayers import fetch_current_players
from getAppDetails import fetch_app_details
from scraping_data_range_wise import scrape
import csv,sys, time, os
from datetime import datetime

# inclusive both , 0 based
# min : 0
# max : 76986
def runner(save_file_name,start=0, end=0):
    with open("data/apps.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        rec = next(reader, False)
        rec = next(reader, False)

        app_ids = []

        # preprocessing
        while rec:
            app_ids.append(rec[1])
            rec = next(reader, False)


        app_id = 730

        res = fetch_app_details(app_id)
        print(res)
        print(len(res))

        '''
            from us : [Index, AppID]
        
            fetch_app_details(22) : [title, initial_price, final_price, discount_percent, developers, publishers, genres, categories, required_age, achievements, release_date, metacritic_score, dlc_flag, win_flag, mac_flag, linux_flag] + (pc_requirements) [os, processor , memory , graphics , directX , storage]

            fetch_current_players : player_count

            scrape(12) : [lang__interface, lang__full_audio, lang__subtitles, positive_reviews, negative_reviews, total_reviews, overall_review_summary,recent_review_count ,recent_review_summary ,m_content, award, curator]
        


        with open(f"fetched-data/{save_file_name}.csv" , "w") as data_file:
            writer = csv.writer(data_file, delimiter="," , lineterminator="\n")

            for idx in range(start, end + 1):
                app_id = app_ids[idx]
                try:
                    row = [idx, app_id]
                    row += fetch_app_details(app_id)
                    # TODO
                    print(app_id)
                except Exception as e:
                    print(f"ERROR at : {app_id}")
                    print(e)
                finally:
                    rec = next(reader, False)
        '''



def main():
    args = sys.argv
    if len(args) > 4:
        print("TOO Many arguments given\nProvide <Your Name> <Start_index> <End_index>\n(Index range to scrape info)")
        return

    if len(args) < 4:
        print("Not enough arguments given\nProvide <Your Name> <Start_index> <End_index>\n(Index range to scrape info)")
        return
    

    # file_name ,name, start, end
    name, start, end = args[1:]
    if not name.isalpha():
        print("Invalid name argument")
        return
    
    if not start.isdigit() or not end.isdigit():
        print("Invalid start or/and end argument(s)")
        return

    start = int(start)
    end = int(end)

    if start > end or start < 0 or end > 76986: 
        print("Invalid start or/and end argument(s) value")
        return
    
    dt =  datetime.now()
    # name,start,end
    save_file_name = f"{start}_{end}_{name}_{dt :%d-%m-%Y_%H-%M-%S}"

    # create directory if not present
    if "fetched-data" not in os.listdir():
        os.mkdir("fetched-data")


    runner(save_file_name, start,end)

if __name__ == "__main__":        
    main()
