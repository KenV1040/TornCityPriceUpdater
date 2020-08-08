from __future__ import print_function
import requests as req
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pickle
import os.path
from google import Create_Service

def main():
    prices = getPrices()
    for k in prices:
        print(f'{k}: {prices[k]}')
    postPrices(prices)

# Sending data from getPrices to my spreadsheet
def postPrices(prices):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)


def getPrices():
    url = 'https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vSkpPkhP41S5r2TpK1FojoQz3lhNJ7MCYbCtOwyvnJOA6aDWy3qTGoA5W6RFbffxclunf387GmJxgBA/pubhtml?gid=972338520&single=true'
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding':'gzip, deflate, br',
        'cache-control':'max-age=0',
        'dnt':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'cookie':'S=apps-spreadsheets=y_zek6Q_uBunJU6FakU7dF1-VFVXGKwUcmA0kclm0Og; OGPC=422038528-1:; CONSENT=YES+GB.en-GB+V9; 1P_JAR=2020-7-14-16; NID=204=EftBMragfVGyJm7LeLF_3XDPAkyJFLpKiAhULau0lVovRo0FcU-pHNpexm37H0fSIcd4SH0uHZjndKq3yPzDgq4hP566iTqOo0Ecr9EzWJUVtduKDRa7z4ZPZMNTTvwkPU4EtTnNeWPwrddEudI0u1qHZU6qslP6qsm_HXOpOwRyo7NKUns',
    }

    resp = req.get(url,headers=headers)
    print(resp.headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    plushies = soup.findAll("td", string=re.compile('(P|p)lushie'))
    tempPrices = {}
    for plushy in plushies:
        parent = plushy.find_parents('tr')
        # Only add rows that has a price
        if plushy.next_sibling.text:
            tempPrices[plushy.text.replace(' Plushie', '')] = plushy.next_sibling.text

    return tempPrices

if __name__ == '__main__':
    main()