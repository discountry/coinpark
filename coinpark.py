import hmac
import hashlib
import json, requests
from random import randint

class Coinpark():
    def __init__(self,base_url = 'https://api.coinpark.cc/v1/'):
        self.base_url = base_url
    
    def auth(self, key, secret):
        self.key = key
        self.secret = secret
    
    def get_signed(self, data):
        signature = hmac.new(self.secret.encode("utf-8"), data.encode("utf-8"), hashlib.md5).hexdigest()
        return signature

    def public_request(self, api_url, cmds):
        s_cmds = json.dumps(cmds)
        r_url = self.base_url + api_url
        r = requests.post(r_url, data={'cmds': s_cmds})
        print(r.text)
        return r.json()
    
    def signed_request(self, api_url, cmds):
        s_cmds = json.dumps(cmds)
        sign = self.get_signed(s_cmds)
        r_url = self.base_url + api_url
        r = requests.post(r_url, data={'cmds': s_cmds, 'apikey': self.key,'sign':sign})
        print(r.text)
        return r.json()
    
    def get_pair_list(self):
        raw_cmds = [{
            'cmd': "api/pairList",
            'body': {}
        }]
        return self.public_request('mdata', raw_cmds)['result']
    
    def get_kline(self, pair, period, size):
        raw_cmds = [{
            'cmd': "api/kline",
            'body': {
                'pair': pair, # BIX_BTC
                'period': period, # ['1min', '3min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '12hour', 'day', 'week']
                'size': size, # 1-1000
            }
        }]
        return self.public_request('mdata', raw_cmds)['result']

    def get_market_data(self):
        raw_cmds = [{
            'cmd': "api/marketAll",
            'body': {}
        }]
        return self.public_request('mdata', raw_cmds)['result']

    def get_pair_data(self, pair):
        raw_cmds = [{
            'cmd': "api/market",
            'body': {
                'pair': pair, # BIX_BTC
            }
        }]
        return self.public_request('mdata', raw_cmds)['result']
    
    def get_pair_depth(self, pair, size):
        raw_cmds = [{
            'cmd': "api/depth",
            'body': {
                'pair': pair, # BIX_BTC
                'size': size, # 1-200
            }
        }]
        return self.public_request('mdata', raw_cmds)['result']
    
    def get_pair_deals(self, pair, size):
        raw_cmds = [{
            'cmd': "api/deals",
            'body': {
                'pair': pair, # BIX_BTC
                'size': size, # 1-200
            }
        }]
        return self.public_request('mdata', raw_cmds)['result']
    
    def get_pair_ticker(self, pair):
        raw_cmds = [{
            'cmd': "api/ticker",
            'body': {
                'pair': pair, # BIX_BTC
            }
        }]
        return self.public_request('mdata', raw_cmds)['result']
    
    def get_assets(self, select = 1):
        raw_cmds = [{
            'cmd': "transfer/assets",
            'body': {
                'select': select, # 可选，1-请求所有币种资产明细，不传-各币种总资产合计
            }
        }]
        return self.signed_request('transfer', raw_cmds)['result']
    
    def get_withdraw(self, id):
        raw_cmds = [{
            'cmd': "transfer/withdrawInfo",
            'body': {
                'id': id, # 提现id
            }
        }]
        return self.signed_request('transfer', raw_cmds)['result']
    
    def post_order(self, pair, account_type, order_type, order_side, pay_bix, price, amount, money):
        raw_cmds = [{
            'cmd': "orderpending/trade",
            'index': randint(1,99999),
            'body': {
                'pair': pair, # BIX_BTC, BIX_ETH
                'account_type': account_type,
                'order_type': order_type,
                'order_side': order_side,
                'pay_bix': pay_bix,
                'price': price,
                'amount': amount,
                'money': money,
            }
        }]
        return self.signed_request('orderpending', raw_cmds)['result']
    
    def limit_buy(self, pair, price, amount):
        return self.post_order(pair, 0, 2, 1, 0, price, amount, None)
    
    def limit_sell(self, pair, price, amount):
        return self.post_order(pair, 0, 2, 2, 0, price, amount, None)

    def market_buy(self, pair, amount, money):
        return self.post_order(pair, 0, 1, 1, 0, None, amount, money)
    
    def market_sell(self, pair, amount, money):
        return self.post_order(pair, 0, 1, 1, 0, None, amount, money)

    def cancel_order(self, orders_id):
        raw_cmds = [{
            'cmd': "orderpending/cancelTrade",
            'index': randint(1,99999),
            'body': {
                'orders_id': orders_id, # 委托id
            }
        }]
        return self.signed_request('orderpending', raw_cmds)['result']
    
    def get_pending_order(self, pair, account_type, page, size, coin_symbol, currency_symbol, order_side):
        raw_cmds = [{
            'cmd': "orderpending/orderPendingList",
            'body': {
                'pair': pair,
                'account_type': account_type,
                'page': page,
                'size': size,
                'coin_symbol': coin_symbol,
                'currency_symbol': currency_symbol,
                'order_side': order_side,
            }
        }]
        return self.signed_request('orderpending', raw_cmds)['result']

    def get_history_order(self, pair, account_type, page, size, coin_symbol, currency_symbol, order_side, hide_cancel = 0):
        raw_cmds = [{
            'cmd': "orderpending/pendingHistoryList",
            'body': {
                'pair': pair,
                'account_type': account_type,
                'page': page,
                'size': size,
                'coin_symbol': coin_symbol,
                'currency_symbol': currency_symbol,
                'order_side': order_side,
                'hide_cancel': hide_cancel,
            }
        }]
        return self.signed_request('orderpending', raw_cmds)['result']

    def get_order_by_id(self, id):
        raw_cmds = [{
            'cmd': "orderpending/order",
            'body': {
                'id': id, # 委托id
            }
        }]
        return self.signed_request('orderpending', raw_cmds)['result']

    def get_order_history_list(self, pair, account_type, page, size, coin_symbol, currency_symbol, order_side):
        raw_cmds = [{
            'cmd': "orderpending/orderHistoryList",
            'body': {
                'pair': pair,
                'account_type': account_type,
                'page': page,
                'size': size,
                'coin_symbol': coin_symbol,
                'currency_symbol': currency_symbol,
                'order_side': order_side,
            }
        }]
        return self.signed_request('orderpending', raw_cmds)['result']
