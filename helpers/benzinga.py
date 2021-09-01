from constants import BENZINGA_GAPPERS

from helpers.misc import extract_using_regex_safe, get_element_safe, getHTMLContent


def _get_gap_links_within_previous_two_days(driver):
    links = []
    for i in range(3):
        URL = f"{BENZINGA_GAPPERS}?page={i}"
        content = getHTMLContent(driver, URL)
        posts_container = get_element_safe(
            content, "div", "benzinga-articles benzinga-articles-mixed"
        )
        posts = posts_container.find_all("li", recursive=True)
        for post in posts:
            try:
                title_container = get_element_safe(post, "h3")
                title_elem = get_element_safe(title_container, "a")
                title = extract_using_regex_safe(
                    r"[0-9]{2}.Stocks Moving [^0-9]+$", title_elem.text
                )
                URL = f"https://www.benzinga.com{title_elem['href']}"
                links.append([title, URL])
            except Exception:
                continue

    # Since there are 2 links per day, skip the first 2 links
    # We only interested in the 2 days ago and 3 days ago
    links = links[2:6]
    result = list(map(lambda x: x[1], links))
    return result


def get_benzinga_gappers(driver):
    result: list[str] = []
    interested_gap_urls = _get_gap_links_within_previous_two_days(driver)

    for recent_gap_url in interested_gap_urls:
        content = getHTMLContent(driver, recent_gap_url)

        stocks_container = get_element_safe(content, "div", "article-content-body-only")
        stocks = stocks_container.find_all("li", recursive=True)

        # DIRECTION_VERBS = BENZINGA_BULL_VERBS + BENZINGA_BEAR_VERBS

        for stock in stocks:
            try:
                ticker_elem = get_element_safe(
                    stock, tag="a", class_="ticker bztwwidgethover", accept_first=True
                )
            except Exception:
                # Sometimes there's a bullet point writing about a stock above it
                continue

            ticker = extract_using_regex_safe(
                r"[A-Z]{1,5}(?:\s*\d{6}[PC]\d{8})?", ticker_elem.text
            )
            # gap_candidates = extract_using_regex_safe(f"({'|'.join(DIRECTION_VERBS)}) (\d*\.?\d+%?)", stock.text)
            # isGoingUp = gap_candidates[0] in BULL_VERBS
            # gap = float(gap_candidates[1].replace("%", ""))
            result.append(ticker.upper())

    result.sort()
    result = list(set(result))
    return result
