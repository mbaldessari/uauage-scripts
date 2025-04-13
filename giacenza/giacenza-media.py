#!/usr/bin/python3

import pandas as pd


# This assumes that the first entry of the day is the last one
# I.e. the CSV is sorted from newest to oldest!
def get_daily_balance(csv_file):
    df = pd.read_csv(csv_file, parse_dates=["Date"], dayfirst=True)
    seen_days = set()
    count = 0
    balance = {}
    for index, row in df.iterrows():
        day = row["Date"]
        if day not in seen_days:
            seen_days.add(day)
            balance[day] = row["Running Balance"]
        else:
            # If we seen this day we skip it (it was the first)
            continue
        count += 1
        # print(row)
        # print(day)

    print(f"TOTAL: {count}")
    return balance


get_daily_balance("~/statement_37543175_GBP_2024-01-01_2024-12-31.csv")
