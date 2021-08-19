import os
import time

from models.webdriver_wrapper import WebDriverWrapper
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
    tickers = []
    qualified_tickers = []

    tickers += get_all_tickers_from_all_market_caps()
    tickers += get_benzinga_gappers(driver)

    print(len(tickers))

    for idx, ticker in enumerate(tickers):
        try:
            tickerSymbol = ticker.upper()
            print(f"{idx + 1}: {tickerSymbol}")
            ohlcv = get_candlestick_data_for_ticker(tickerSymbol)
            if check_if_is_3_bar_play(ohlcv) and check_if_has_acceptable_spreads(
                tickerSymbol
            ):
                qualified_tickers.append(tickerSymbol)
            time.sleep(1.5)
            break
        except Exception:
            break

    new_file_name = f"{get_date_before_current().strftime('%Y-%m-%d')}.txt"
    new_file_path = os.path.join("out", new_file_name)
    with open(new_file_path, "w+") as f:
        for qualified_ticker in qualified_tickers:
            f.write(f"{qualified_ticker}\n")


main()
