import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from time import time
from time import sleep
from random import randint
import pandas as pd
import tweepy
import re
from os import environ

CONSUMER_API_KEY = environ['CONSUMER_API_KEY']
CONSUMER_API_SECRET_KEY = environ['CONSUMER_API_SECRET_KEY']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_SECRET_TOKEN = environ['ACCESS_SECRET_TOKEN']

auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
api = tweepy.API(auth)

base_url = 'https://spotifycharts.com/regional/jp/daily/latest/'
start = (date.today() - timedelta(days = 1))
end = date.today()

skip = {date(2017, 2, 23), date(2017, 5, 30), date(2017, 5, 31), date(2017, 6, 2),
        date(2017, 7, 20), date(2017, 7, 21), date(2017, 7, 22), date(2017, 7, 23),
        date(2017, 11, 9), date(2017, 11, 10), date(2017, 11, 11), date(2017, 11, 12),
        date(2017, 11, 13), date(2017, 11, 14), date(2017, 12, 1), date(2019, 4, 5)}
iter = timedelta(days = 1)

start_time = time()
serve = 0

mydate = start

while mydate < end:

    while mydate in skip:
        mydate += iter

    if(mydate > end):
        break

    r = requests.get(base_url + mydate.strftime('%Y-%m-%d'))
    mydate += iter

    sleep(randint(1,3))

    serve += 1
    elapsed_time = time() - start_time

    soup = BeautifulSoup(r.text, 'html.parser')

    chart = soup.find('table', {'class': 'chart-table'})

    tbody = chart.find('tbody')

    all_rows = []

    for tr in tbody.find_all('tr'):

        rank_text = tr.find('td', {'class': 'chart-table-position'}).text

        artist_text = tr.find('td', {'class': 'chart-table-track'}).find('span').text
        artist_text = artist_text.replace('by ','').strip()
        
        if artist_text == 'Official HIGE DANdism':
            artist_text = 'Official髭男dism'
        if artist_text == 'Eito':
            artist_text = '瑛人'
        if artist_text == 'Kenshi Yonezu':
            artist_text = '米津玄師'

        title_text = tr.find('td', {'class': 'chart-table-track'}).find('strong').text
        
        if title_text == 'Kanden':
            title_text = '感電'
        if title_text == 'Machigai Sagashi':
            title_text = 'まちがいさがし'
        if title_text == 'Campanella':
            title_text = 'カムパネルラ'
        if title_text == 'Uma to Shika':
            title_text = '馬と鹿'
        if title_text == 'Yasashii Hito':
            title_text = '優しい人'
        if title_text == 'Himawari':
            title_text = 'ひまわり'
        if title_text == 'Spirits of the Sea':
            title_text = '海の幽霊'
        if title_text == 'Shukumei':
            title_text = '宿命'
        if title_text == 'Yesterday':
            title_text = 'イエスタデイ'
            
        streams_text = tr.find('td', {'class': 'chart-table-streams'}).text
        
        first_link = tr.find('td', {'class': 'chart-table-image'}).find_all('a', href=True)

        date = (mydate - iter)

        all_rows.append( [rank_text, artist_text, title_text, streams_text, date.strftime('%Y-%m-%d'), first_link] )

    df = pd.DataFrame(all_rows, columns =['Rank','Artist','Title','Streams', 'Date', 'Link'])
    print(df)

    first = "[1]" + " " + df['Title'].iloc[0] + " / " + df['Artist'].iloc[0] + "\n" + df['Streams'].iloc[0]
    second = "[2]" + " " + df['Title'].iloc[1] + " / " + df['Artist'].iloc[1] + "\n" + df['Streams'].iloc[1]
    third = "[3]" + " " + df['Title'].iloc[2] + " / " + df['Artist'].iloc[2] + "\n" + df['Streams'].iloc[2]
    fourth = "[4]" + " " + df['Title'].iloc[3] + " / " + df['Artist'].iloc[3] + "\n" + df['Streams'].iloc[3]
    fifth = "[5]" + " " + df['Title'].iloc[4] + " / " + df['Artist'].iloc[4] + "\n" + df['Streams'].iloc[4]
    sixth = "[6]" + " " + df['Title'].iloc[5] + " / " + df['Artist'].iloc[5] + "\n" + df['Streams'].iloc[5]
    seventh = "[7]" + " " + df['Title'].iloc[6] + " / " + df['Artist'].iloc[6] + "\n" + df['Streams'].iloc[6]
    eighth = "[8]" + " " + df['Title'].iloc[7] + " / " + df['Artist'].iloc[7] + "\n" + df['Streams'].iloc[7]
    nineth = "[9]" + " " + df['Title'].iloc[8] + " / " + df['Artist'].iloc[8] + "\n" + df['Streams'].iloc[8]
    tenth = "[10]" + " " + df['Title'].iloc[9] + " / " + df['Artist'].iloc[9] + "\n" + df['Streams'].iloc[9]

    first_link = (str(df['Link'].iloc[0]))[10:63]
    sixth_link = (str(df['Link'].iloc[5]))[10:63]
 
##    status = api.update_status(first + '\n' + second + '\n' + third + '\n' + fourth + '\n' + fifth + '\n' + first_link)
##    status2 = api.update_status(('@SpotifyRankJP' + ' ' + sixth + '\n' + seventh + '\n' + eighth + '\n' + nineth + '\n' + tenth + '\n' + sixth_link), status.id)












