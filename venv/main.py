from __future__ import print_function
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def main():
    prices = getPrices()
    for k in prices:
        print(f'{k}: {prices[k]}')
    postPrices(prices)

# Sending data from getPrices to my spreadsheet
def postPrices(prices):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1p4lehLDD8ZkHhDyj_l337u7GeaDzv7exczYK2gCM'
    SAMPLE_RANGE_NAME = 'Class Data!A2:E'

    # Set up connection to google sheets api
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


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

    resp = requests.get(url,headers=headers)
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