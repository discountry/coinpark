#!/usr/bin/python3

from coinpark import Coinpark

coinpark = Coinpark()

coinpark.get_pair_list()

coinpark.get_kline('BIX_BTC', '1min', 10)
