#!/usr/bin/python3

import argparse
import sys

import pandas as pd

EUROXREF_URL = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
EUROXREF_FILE = "./eurofxref-hist.csv"

euroxref = pd.read_csv(EUROXREF_FILE, parse_dates=["Date"])

latest_date = euroxref["Date"].max()
today = pd.Timestamp.today().normalize()
if (today - latest_date).days > 3:
    print(f"WARNING: {EUROXREF_FILE} latest data is from {latest_date.date()}, which is more than 3 days old.")
    print(f"Download an updated file from:\n  {EUROXREF_URL}")
    sys.exit(1)


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


parser = argparse.ArgumentParser(description="Calculate giacenza media in EUR from a GBP bank statement CSV.")
parser.add_argument("csv_file", help="Path to the bank statement CSV file")
args = parser.parse_args()

bal = get_daily_balance(args.csv_file)
print(f"Giacenza media in EUR: {get_giacenza_media(bal)}")
