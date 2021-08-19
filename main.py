import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api.finnhub import get_candlestick_data_for_ticker
from api.tda import check_if_has_acceptable_spreads
from helpers.benzinga import get_benzinga_gappers
from helpers.misc import (
    get_all_tickers_from_all_market_caps,
    get_date_before_current,
    isWeekday,
)
from helpers.quant import check_if_is_3_bar_play


def main():
    # Skip if it's weekend
    if not isWeekday():
        return

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome("./assets/chromedriver")

    # For debuggin
    df = pd.DataFrame()
    is_3_bar_play_list: list[bool] = []
    has_acceptable_spread_list: list[bool] = []

    tickers = []
    qualified_tickers = []

    tickers += get_all_tickers_from_all_market_caps()
    tickers += get_benzinga_gappers(driver)
    df["Ticker"] = pd.Series(tickers)

    for idx, ticker in enumerate(tickers):
        try:
            tickerSymbol = ticker.upper()
            print(f"{idx + 1}: {tickerSymbol}")
            ohlcv = get_candlestick_data_for_ticker(tickerSymbol)
            is_3_bar_play_list.append(check_if_is_3_bar_play(ohlcv))
            has_acceptable_spread_list.append(
                check_if_has_acceptable_spreads(tickerSymbol)
            )
            if is_3_bar_play_list[-1] and has_acceptable_spread_list[-1]:
                qualified_tickers.append(tickerSymbol)
            time.sleep(1.5)
        except Exception:
            print("error")
            break

    new_debug_file_name = f"{get_date_before_current().strftime('%Y-%m-%d_debug')}.txt"
    new_debug_file_path = os.path.join("out", new_debug_file_name)
    new_file_name = f"{get_date_before_current().strftime('%Y-%m-%d')}.txt"
    new_file_path = os.path.join("out", new_file_name)
    with open(new_file_path, "w+") as f:
        for qualified_ticker in qualified_tickers:
            f.write(f"{qualified_ticker}\n")

    df["Is 3/4 bar play"] = pd.Series(is_3_bar_play_list)
    df["Has acceptable spreads"] = pd.Series(has_acceptable_spread_list)
    df.to_csv(new_debug_file_path, index=False)


main()
