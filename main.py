import requests as r
import datetime as dt
import sys
import time

RETRY_SEC = 10
NUM_NIGHTS_REQUIRED = 8
earliest_date = '2022-01-01'
latest_date = '2022-01-24'
cities = [
    'taipei-city',
    'taoyuan-city',
    'kaohsiung-city',
    'taichung-city',
    'tainan-city',
    'yilan-county',
    'new-taipei-city',
    'changhua-county',
    'nantou-county',
    'taitung-county',
    'hualien-county',
]

DATE_STR_FORMAT = '%Y-%m-%d'
def getRes(url):
    while True:
        res = r.get(url)
        j = res.json()
        if 'totalBnbs' in j['data'].keys():
            return j
        elif 'status' in j.keys():
            if j['status']['msg'] == 'Too Many Requests':
                print("Too many requests... Retry after {} secs...".format(RETRY_SEC))
                time.sleep(RETRY_SEC)
            else:
                sys.exit('unexpected error occurred!! {}'.format(j))
        else:
            sys.exit('unexpected error occurred!! {}'.format(j))

def search_rooms(city, checkInOn):
    start_date = dt.datetime.strptime(checkInOn, DATE_STR_FORMAT)
    end_date = start_date + dt.timedelta(days=NUM_NIGHTS_REQUIRED)
    url = 'https://web-api.asiayo.com/api/v1/bnbs/search?locale=zh-tw&currency=HKD&people=1&type=city&country=tw&tags=quarantine-hotel&offset=0&limit=21&sortBy=ayscore'
    url += '&city={}'.format(city)
    url += '&checkInDate={}'.format(start_date.strftime(DATE_STR_FORMAT))
    url += '&checkOutDate={}'.format(end_date.strftime(DATE_STR_FORMAT))
    j = getRes(url)
    meta = "[{}/{}-{}]".format(city, start_date.strftime('%b%d'), end_date.strftime('%b%d'))
    print("{} totalBnbs: {} totalRooms: {}".format(meta, j['data']['totalBnbs'], j['data']['totalRooms']))
    ## Print hotel names if results found 
    if j['data']['totalRooms'] > 0:
        for row in j['data']['rows']:
            print("Name: {}".format(row['name']))


for city in cities:
    print("\nCity: {}".format(city))
    i = 0
    while True:
        start_date = dt.datetime.strptime(earliest_date, DATE_STR_FORMAT) + dt.timedelta(days=i)
        start_date_str = start_date.strftime(DATE_STR_FORMAT)
        search_rooms(city, start_date_str)
        if start_date_str == latest_date:
            break
        i+=1
