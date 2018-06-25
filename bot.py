#!/usr/bin/python3

from coinpark import Coinpark
import schedule
import time
from decimal import Decimal, ROUND_HALF_EVEN

coinpark = Coinpark()

coinpark.auth('xxx', 'xxx')

pair = 'ETH_USDT'
price_precision = '.01'
amount = 1000

def handler():
    ticker = coinpark.get_pair_ticker(pair)
    buy = ticker['buy']
    print('buy_price', buy)
    sell = ticker['sell']
    print('sell_price', sell)
    margin = buy - sell

    if margin > 0:
        coinpark.batch_limit_buy_sell(pair, Decimal((buy + sell) / 2).quantize(Decimal(price_precision), rounding=ROUND_HALF_EVEN), amount)

schedule.every(1).seconds.do(handler)

while True:
    schedule.run_pending()
    time.sleep(1)
