import csv


def scrape(app_id):
    '''
        yaha likh kanak apna code to scrape <app_id> details and write to a csv
    '''
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


main()
