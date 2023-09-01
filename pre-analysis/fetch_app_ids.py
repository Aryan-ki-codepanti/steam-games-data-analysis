import csv


def fetch_app_ids():
    with open("data/games.csv", "r", encoding="utf8") as f:
        with open("data/app_ids.csv", "w", encoding="utf8") as f2:
            reader = csv.reader(f)
            writer = csv.writer(f2, lineterminator="\n")

            record = next(reader, False)
            while record:
                writer.writerow([record[0]])
                record = next(reader, False)


fetch_app_ids()
