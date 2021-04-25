import logging
import os
from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep

import pandas as pd
import pytz
import requests
from bs4 import BeautifulSoup

import config
from kiteext import KiteExt

log = logging.getLogger(__name__)
# NOTE while creating date objects you can use zone info which is very helpful when you are running scripts on outside India location
zone = pytz.timezone('Asia/Kolkata')

if __name__ == "__main__":
    global kite

    begin_time = dt.now(tz=zone)
    print(begin_time)

    kite = KiteExt(userid=config.username)
    kite.login_with_credentials(config.username, config.password, config.pin)
    margins = kite.margins()
    net_balance_equity = margins['equity']['net']
    live_balance_equity = margins['equity']['available']['live_balance']

    print(net_balance_equity)
    print(live_balance_equity)

    end_time = dt.now(tz=zone)
    duration = (end_time - begin_time)

    print(f'Total time taken by script :: {duration}')
