#!/usr/bin/python3

import pandas as pd


# Time series to be downloaded from
# https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html
euroxref = pd.read_csv("./eurofxref-hist.csv", parse_dates=["Date"])


def get_daily_eur_gbp(day, currency="GBP"):
    newday = day
    while True:
        result = euroxref[euroxref["Date"] == newday]
        if len(result) > 1:
            raise Exception("Result more than one line for: %s" % newday)
        # The euroxref only contains working days so we will take the first
        # next available exchange rate
        if result.empty:
            newday = newday - pd.Timedelta(days=1)
        else:
            break
        if newday < pd.Timestamp("1999-01-04"):
            raise Exception("Something very wrong happened: %s" % newday)

    rate = result.iloc[0]["GBP"]
    # print(f"Asked for day: {day} Got: {newday} -> {rate}")
    return rate


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
            xchange = get_daily_eur_gbp(day)
            euros = row["Running Balance"] / xchange
            balance[day] = euros
        else:
            # If we seen this day we skip it (it was the first)
            continue
        count += 1
        # print(f"GBP: {xchange}")

    print(f"TOTAL: {count}")
    return balance


def get_giacenza_media(b):
    return sum(b.values()) / len(b)


bal = get_daily_balance("~/statement_37543175_GBP_2024-01-01_2024-12-31.csv")
print(f"Giacenza media in EUR: {get_giacenza_media(bal)}")
