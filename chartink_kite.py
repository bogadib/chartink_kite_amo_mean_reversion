import pytz
import pandas as pd
import requests
from bs4 import BeautifulSoup

import os

from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep

import config
import logging


from kiteext import KiteExt


log = logging.getLogger(__name__)


# NOTE while creating date objects you can use zone info which is very helpful when you are running scripts on outside India location
zone = pytz.timezone('Asia/Kolkata')

start = dt.now(tz=zone)
print(start)


def get_stocks():

    with requests.Session() as s:
        scanner_url = 'https://chartink.com/screener/vishal-mehta-mean-reversion'
        r = s.get(scanner_url)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf

        process_url = 'https://chartink.com/screener/process'
        payload = {
            # NOTE Vishal Mehta Mean Reversion Selling - Place Limit Order at 1% of Latest Close Price 3% SL and 6% Target Exit all positions at 3PM
            'scan_clause': '( {33489} ( latest close > latest sma( close,200 ) and latest rsi( 2 ) > 50 and '\
            'latest close > 1 day ago close * 1.03 and latest close > 200 and latest close < 2000 and latest close > ( 4 days ago close * 1.0 ) ) ) '
        }

        r = s.post(process_url, data=payload)
        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
        # NOTE Sorting done by ascending price so that stock with less price can be purchased before
        # Costly stocks may be rejected if there is no capital
        df.sort_values(by=['close'], inplace=True)
        df.drop('sr', axis=1, inplace=True)
        df.reset_index(inplace=True)
        df.drop('index', axis=1, inplace=True)

        if len(df) > 10:
            print(f'number of stocks :: {len(df)}')
            df = df.head(10)
        return df


def capital_per_stock(balance, factor):
    return round(float(balance / factor), 0)


# variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price=None,
# validity=None, disclosed_quantity=None, trigger_price=None, squareoff=None, stoploss=None, trailing_stoploss=None, tag=None)


def place_amo_limit_order(symbol, price, qty):
    global kite
    # NOTE :: Need to place Limit Sell Order, Change PRODUCT to NRML to avoid leverage
    price = round((price * 1.01), 1)

    return kite.place_order(transaction_type=kite.TRANSACTION_TYPE_SELL, tradingsymbol=symbol, quantity=qty, price=price,
                            product=kite.PRODUCT_MIS, order_type=kite.ORDER_TYPE_LIMIT, variety=kite.VARIETY_AMO, exchange=kite.EXCHANGE_NSE)


def place_amo_orders(stocks):
    order_ids = []
    stocks.rename(columns={'nsecode': 'symbol',
                  'close': 'price'}, inplace=True)
    # print(stocks)
    for stock in stocks.itertuples():
        print(stock.symbol, stock.price, stock.qty)
        order = place_amo_limit_order(stock.symbol, stock.price, stock.qty)
        order_ids.append(order)
        sleep(0.2)

    return order_ids

def get_amo_orders():
    global kite
    data = kite.orders()
    df = pd.DataFrame(data, index=None)
    df = df[['exchange', 'tradingsymbol', 'order_type', 'quantity', 'variety', 'status', 'order_id', 'order_timestamp', 'product', 'transaction_type']]
    df = df.loc[df['status'] == 'AMO REQ RECEIVED']
    return df

if __name__ == "__main__":
    global kite

    stocks = get_stocks()
    print(stocks)

    kite = KiteExt(userid=config.username)
    kite.set_headers(config.enctoken)
    margins = kite.margins()
    net_balance_equity = margins['equity']['net']
    # live_balance_equity = margins['equity']['available']['live_balance']

    print(net_balance_equity)
    # print(live_balance_equity)

    # capital = capital_per_stock(net_balance_equity, len(stocks)) # If you want to allocate as per stock
    net_balance_equity = 50000.0  # for the sake of calculation
    capital = capital_per_stock(net_balance_equity, 10)

    stocks['qty'] = capital / stocks['close']
    stocks['qty'] = stocks['qty'].astype(int).round(0)
    stocks = stocks[['nsecode', 'close', 'qty', 'per_chg', 'volume']]

    print(stocks)
    # orders_ids = place_amo_orders(stocks)
    # sleep(2)
    # print(orders_ids)
    print(get_amo_orders())
