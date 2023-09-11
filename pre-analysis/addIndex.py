import pandas as pd

def add_index():
    df = pd.read_csv("data/app_ids.csv")
    df["Index"] = 0
    for i in range(len(df)):
        print(i)
        df["Index"][i] = i

    df[["Index", "AppID"]].to_csv("data/apps.csv", index=False)
    
if __name__ == "__main__":
    add_index()
    
