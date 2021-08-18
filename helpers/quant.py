import math

import pandas as pd


def check_if_is_3_bar_play(ohlcv):
    open = pd.Series(list(reversed(ohlcv["o"])))
    high = pd.Series(list(reversed(ohlcv["h"])))
    low = pd.Series(list(reversed(ohlcv["l"])))
    close = pd.Series(list(reversed(ohlcv["c"])))

    if len(open) < 7:
        return False

    barSize = abs(high - low)
    bodySize = abs(open - close)

    averageBodySize = []
    for i in range(len(barSize)):
        try:
            bodySizeSum = 0.0
            for j in range(i + 1, i + 6):
                bodySizeSum += barSize[j]
            averageBodySize.append(bodySizeSum / 5)
        except KeyError:
            averageBodySize.append(math.inf)

    averageBodySize = pd.Series(averageBodySize)

    isWideRangeBar = bodySize > averageBodySize * 1.5

    collectingBarBull = []
    for i in range(len(high)):
        try:
            result = (
                (high[i] <= high[i + 1] + barSize[i] * 0.4)
                & (high[i] >= high[i + 1] - barSize[i] * 0.4)
                & (low[i] >= ((barSize[i + 1] / 2) + low[i + 1]))
            )
            collectingBarBull.append(result)
        except KeyError:
            collectingBarBull.append(False)
    collectingBarBull = pd.Series(collectingBarBull)

    collectingBarBull2 = []
    for i in range(len(high)):
        try:
            result = (
                (high[i] <= high[i + 2] + barSize[i] * 0.4)
                & (high[i] >= high[i + 2] - barSize[i] * 0.4)
                & (low[i] >= ((barSize[i + 2] / 2) + low[i + 2]))
            )
            collectingBarBull2.append(result)
        except KeyError:
            collectingBarBull2.append(False)
    collectingBarBull2 = pd.Series(collectingBarBull2)

    collectingBarBear = []
    for i in range(len(low)):
        try:
            result = (
                (low[i] >= low[i + 1] - barSize[i] * 0.4)
                & (low[i] <= low[i + 1] + barSize[i] * 0.4)
                & (high[i] <= ((barSize[i + 1] / 2) + low[i + 1]))
            )
            collectingBarBear.append(result)
        except KeyError:
            collectingBarBear.append(False)
    collectingBarBear = pd.Series(collectingBarBear)

    collectingBarBear2 = []
    for i in range(len(low)):
        try:
            result = (
                (low[i] >= low[i + 2] - barSize[i] * 0.4)
                & (low[i] <= low[i + 2] + barSize[i] * 0.4)
                & (high[i] <= ((barSize[i + 2] / 2) + low[i + 2]))
            )
            collectingBarBear2.append(result)
        except KeyError:
            collectingBarBear2.append(False)
    collectingBarBear2 = pd.Series(collectingBarBear2)

    result = []
    for i in range(len(isWideRangeBar)):
        try:
            temp = (
                (
                    isWideRangeBar[i + 1]
                    & collectingBarBull[i]
                    & (close[i + 1] > open[i + 1])
                )
                | (
                    isWideRangeBar[i + 2]
                    & collectingBarBull[i + 1]
                    & collectingBarBull2[i]
                    & (close[i + 2] > open[i + 2])
                )
                | (
                    isWideRangeBar[i + 1]
                    & collectingBarBear[i]
                    & (close[i + 1] < open[i + 1])
                )
                | (
                    isWideRangeBar[i + 2]
                    & collectingBarBear[i + 1]
                    & collectingBarBear2[i]
                    & (close[i + 2] < open[i + 2])
                )
            )
            result.append(temp)
        except KeyError:
            result.append(False)

    result = pd.Series(result)
    return result[0]
