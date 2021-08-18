import os

import requests
from constants import FINNHUB_API_BASE
from dotenv.main import load_dotenv
from helpers.misc import get_date_timestamp_in_seconds_before_current


def _check_if_ticker_is_invalid_or_timeout(data):
    return data["s"] == "no_data"


def get_candlestick_data_for_ticker(tickerSymbol):
    load_dotenv(dotenv_path=".env")

    API_KEY = os.environ["FINNHUB_API_KEY"]
    fromTimestamp = get_date_timestamp_in_seconds_before_current(14)
    toTimestamp = get_date_timestamp_in_seconds_before_current(0)
    URL = f"{FINNHUB_API_BASE}/stock/candle?symbol={tickerSymbol}&resolution=D&from={fromTimestamp}&to={toTimestamp}&token={API_KEY}"  # noqa: E501

    response = requests.request("GET", URL)
    data = response.json()

    if _check_if_ticker_is_invalid_or_timeout(data):
        raise Exception("Invalid ticker or quota exceeded")

    return data
