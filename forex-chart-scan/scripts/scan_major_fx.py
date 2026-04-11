from __future__ import annotations

import argparse
import os
import time

from data_fetcher import TVDataFetcher
from profiles import detect_aim_for_range_high, detect_aim_for_range_low
from seek_and_destroy import detect_seek_and_destroy

DEFAULT_EXCHANGE = "FOREXCOM"

MAJOR_FX_PAIRS = [
    ("EURUSD", DEFAULT_EXCHANGE),
    ("GBPUSD", DEFAULT_EXCHANGE),
    ("USDJPY", DEFAULT_EXCHANGE),
    ("AUDUSD", DEFAULT_EXCHANGE),
    ("NZDUSD", DEFAULT_EXCHANGE),
    ("USDCAD", DEFAULT_EXCHANGE),
    ("USDCHF", DEFAULT_EXCHANGE),
    ("EURJPY", DEFAULT_EXCHANGE),
    ("EURGBP", DEFAULT_EXCHANGE),
    ("EURCHF", DEFAULT_EXCHANGE),
    ("EURAUD", DEFAULT_EXCHANGE),
    ("EURNZD", DEFAULT_EXCHANGE),
    ("EURCAD", DEFAULT_EXCHANGE),
    ("GBPJPY", DEFAULT_EXCHANGE),
    ("GBPCHF", DEFAULT_EXCHANGE),
    ("GBPAUD", DEFAULT_EXCHANGE),
    ("GBPNZD", DEFAULT_EXCHANGE),
    ("GBPCAD", DEFAULT_EXCHANGE),
    ("AUDJPY", DEFAULT_EXCHANGE),
    ("AUDNZD", DEFAULT_EXCHANGE),
    ("AUDCAD", DEFAULT_EXCHANGE),
    ("AUDCHF", DEFAULT_EXCHANGE),
    ("NZDJPY", DEFAULT_EXCHANGE),
    ("NZDCAD", DEFAULT_EXCHANGE),
    ("NZDCHF", DEFAULT_EXCHANGE),
    ("CADJPY", DEFAULT_EXCHANGE),
    ("CHFJPY", DEFAULT_EXCHANGE),
]


def _batched(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def scan(
    timeframe: str = "1D",
    bars: int = 5,
    trim_ongoing: int = 1,
    batch_size: int = 9,
    sleep_between_batches: float = 2.0,
):
    fetcher = TVDataFetcher()
    results = []
    for batch in _batched(MAJOR_FX_PAIRS, batch_size if batch_size > 0 else len(MAJOR_FX_PAIRS)):
        for symbol, exchange in batch:
            df = fetcher.fetch(symbol=symbol, exchange=exchange, timeframe=timeframe, bars=bars)
            if trim_ongoing > 0 and len(df) > trim_ongoing:
                df = df.iloc[:-trim_ongoing]

            snd = detect_seek_and_destroy(df)
            arl = detect_aim_for_range_low(df)
            arh = detect_aim_for_range_high(df)

            results.append(
                {
                    "symbol": symbol,
                    "seek_and_destroy": bool(snd.iloc[-1]) if len(snd) else False,
                    "aim_for_range_low": bool(arl.iloc[-1]) if len(arl) else False,
                    "aim_for_range_high": bool(arh.iloc[-1]) if len(arh) else False,
                }
            )
        if sleep_between_batches > 0:
            time.sleep(sleep_between_batches)
    return results


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan major FX pairs for long-term ICT concepts.")
    parser.add_argument("--timeframe", default=os.getenv("SCAN_TIMEFRAME", "1D"), help="tvDatafeed timeframe, e.g. 1D, 1W, 1M")
    parser.add_argument("--bars", type=int, default=int(os.getenv("SCAN_BARS", "5")), help="Number of candles to fetch")
    parser.add_argument("--trim-ongoing", type=int, default=int(os.getenv("SCAN_TRIM_ONGOING", "1")), help="How many latest candles to trim before scanning")
    parser.add_argument("--batch-size", type=int, default=int(os.getenv("SCAN_BATCH_SIZE", "9")), help="Pairs per batch")
    parser.add_argument("--sleep-between-batches", type=float, default=float(os.getenv("SCAN_SLEEP_BETWEEN_BATCHES", "2")), help="Seconds to sleep between batches")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    for row in scan(
        timeframe=args.timeframe,
        bars=args.bars,
        trim_ongoing=args.trim_ongoing,
        batch_size=args.batch_size,
        sleep_between_batches=args.sleep_between_batches,
    ):
        print(row)
