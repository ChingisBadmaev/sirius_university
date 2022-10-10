import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://finance.yahoo.com/quote/%5EGSPC/history?period1=1268179200&period2=1665360000&interval=1d&filter' \
      '=history&frequency=1d&includeAdjustedClose=true '
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}
FILE = 's_and_p_index_data.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items_quote_data = soup.find_all('table', class_='W(100%) M(0)')
    for item in items_quote_data:
        one_day_data = item.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')
        for values in one_day_data:
            print(values.find('td', class_='Py(10px) Ta(start) Pend(10px)').get_text())  # get date

            # all data has the same class, so it will pass through find_all
            prices = values.find_all('td', class_='Py(10px) Pstart(10px)')
            for price in prices:
                print(price.get_text())
            print()
        # print(item.get_text(), end='\n')


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        print('Error')


parse()
