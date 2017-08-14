import requests
import pandas as pd
import xml.etree.ElementTree as ET


def get_currencies_dict():
    """
    Справочник получения списка валют с ISO кодами
    :return: Pandas dataframe
    """

    url = 'http://www.cbr.ru/scripts/XML_valFull.asp'
    currencies_dict = requests.get(url)

    # Список валют
    currencies_list = []

    root = ET.fromstring(currencies_dict.text)
    for child in root:
        eng_name = child[1].text
        nominal = child[2].text
        cb_code = child.attrib['ID']
        iso_num_code = child[4].text
        iso_code = child[5].text

        currencies_list.append([eng_name, nominal, cb_code, iso_num_code, iso_code])

    return pd.DataFrame(currencies_list, columns=['eng_name', 'nominal', 'cb_code', 'iso_num_code', 'iso_code'])


def get_currency_listing(currency):
    """
    Получение котировок валюты
    :param currency: Ид валюты (cb_code)
    :return:
    """

    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

    payload = {
        'date_req1': '01/01/2015',
        'date_req2': '30/12/2018',
        'VAL_NM_RQ': currency
    }
    r = requests.get(url, payload)

    root = ET.fromstring(r.text)

    # Котировки валюты
    listing = []
    for child in root:
        date = child.attrib['Date']
        nominal = child[0].text
        value = child[1].text
        listing.append([date, nominal, value])

    return pd.DataFrame(listing, columns=['date', 'nominal', 'value'])

currencies_dict = get_currencies_dict()

"""
Для каждой валюты выгружаем листинг котировок
"""
dfs = []
for i, row in currencies_dict.iterrows():
    listing = get_currency_listing(row['cb_code'])

    listing['cb_code'] = row['cb_code']
    listing['iso_code'] = row['iso_code']
    listing['iso_num_code'] = row['iso_num_code']

    dfs.append(listing)

df = pd.concat(dfs).fillna(0)

df.date = pd.to_datetime(df.date, format='%d.%m.%Y')
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year
df['value'] = df.value.str.replace(',', '.').astype('float')
df['value'] = df.value/df.nominal.astype('float')

df = df[['date', 'value', 'cb_code', 'iso_num_code', 'iso_code', 'month', 'year']]
agg = df.groupby(['month', 'year', 'iso_code']).mean().reset_index()

from_date = str(df.date.unique()[0])[:7]
to_date = str(df.date.unique()[-1])[:7]

print(agg)

agg.to_csv('currencies_monthly_list_{0}_{1}.tsv'.format(from_date, to_date), sep='\t', index=False)

