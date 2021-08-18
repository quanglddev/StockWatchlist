import datetime
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from constants import NASDAQ_MARKET_CAPS


def get_tickers_from_cap_list(cap_name):
    df = pd.read_csv(f"assets/{cap_name.upper()}.csv")
    all_symbols = df["Symbol"]

    return all_symbols.tolist()


def get_all_tickers_from_all_market_caps():
    result: list[str] = []
    for market_cap in NASDAQ_MARKET_CAPS:
        result += get_tickers_from_cap_list(market_cap)
    return result


def getHTMLContent(driver, URL):
    driver.get(URL)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup


def extract_using_regex_safe(pattern, text):
    candidates = re.findall(pattern, text)
    if len(candidates) == 0:
        raise Exception(f"Cannot find text matching pattern: {pattern}")
    elif len(candidates) > 1:
        print("WARNING: More than 1 found. Please avoid this function!")
    else:
        return candidates[0]


def get_element_safe(source, tag, class_=None, recursive=True):
    if class_ is None:
        filtered = source.find_all(tag, recursive=recursive)
    else:
        filtered = source.find_all(tag, class_=class_, recursive=recursive)
    if len(filtered) == 0:
        raise Exception("Cannot find element: <{tag} class='{class_}'></{tag}>")
    elif len(filtered) > 1:
        print("WARNING: More than 1 element found. Please avoid this function!")
    else:
        return filtered[0]


def get_date_timestamp_in_seconds_before_current(distance_day=0):
    current_date = datetime.datetime.now()
    delta = datetime.timedelta(days=distance_day)
    result_date = current_date - delta
    return int(result_date.timestamp())


def get_date_before_current(distance_day=0):
    current_date = datetime.datetime.now()
    delta = datetime.timedelta(days=distance_day)
    result_date = current_date - delta
    return result_date


def isWeekday():
    weekno = datetime.datetime.today().weekday()
    return weekno < 5
