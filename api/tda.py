import os

import requests
from constants import ACCEPTABLE_SPREADS, TDA_API_BASE
from dotenv.main import load_dotenv
from helpers.misc import get_date_before_current


def _check_if_ticker_has_options(data):
    return data["status"] == "SUCCESS"


def _check_if_option_strategy_has_acceptable_spreads(data, strategy):
    contractsMap = data[f"{strategy.lower()}ExpDateMap"]
    for expKey in contractsMap:
        for strikeKey in contractsMap[expKey]:
            contracts = contractsMap[expKey][strikeKey]
            if len(contracts) == 0:
                return False

            contract = contracts[0]
            bid = contract["bid"]
            ask = contract["ask"]

            if abs(bid - ask) <= ACCEPTABLE_SPREADS:
                return True
    return False


def check_if_has_acceptable_spreads(tickerSymbol):
    load_dotenv(dotenv_path=".env")

    API_KEY = os.environ["TDA_API_KEY"]
    fromDate = get_date_before_current(0).strftime("%Y-%m-%d")
    toDate = get_date_before_current(-31).strftime("%Y-%m-%d")
    URL = f"{TDA_API_BASE}/marketdata/chains?apikey={API_KEY}&symbol={tickerSymbol}&strikeCount=2&fromDate={fromDate}&toDate={toDate}"  # noqa: E501

    response = requests.request("GET", URL)
    data = response.json()

    if not _check_if_ticker_has_options(data):
        return False

    is_put_acceptable = _check_if_option_strategy_has_acceptable_spreads(data, "put")
    is_call_acceptable = _check_if_option_strategy_has_acceptable_spreads(data, "call")

    return is_put_acceptable or is_call_acceptable
