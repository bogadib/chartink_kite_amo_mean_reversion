from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os

username=os.getenv('USERNAME')
password=os.getenv('PASSWORD')
pin=os.getenv('PIN')

try:
    enctoken = open('enctoken.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    enctoken = None
