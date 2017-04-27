import requests
import csv
from bs4 import BeautifulSoup

payload = {
    'ctl00_ContentPlaceHolder1_TSM_HiddenField':';;AjaxControlToolkit, Version=3.5.60919.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:1b2a7bd0-6032-4300-93ff-58bf8356d8f8:de1feab2:fcf0e993:f2c8e708:720a52bf:f9cec9bc:589eaa30:698129cf:fb9b4c57:ccb96cf9',
    '__VIEWSTATE': 'mA7VY2YWDScE9iiVltU7xtCZgEvaYv9fxWewhxtd7M2kGOSbalK7rxMWREgPg/OBMCz0NmF/4ZSeeqX6Ydbp24Fc3006IDlb7yegV8QwjjHoerI/KDo6KRmJPNs7ke2Udxc60LIsSgDFMib1o5cAco4HILi1IMX3J6VMzjLig2SweYb6gpAitvML9ytyjWaR1pTR97eXhP1e2V/aNweFyCqw4gZbyZdnSaCx96scaZnkV4BrsR3DgV4KuW3mfnEUuHIPWpfqdTH9G63+Scspp4KPeQfJRXXiMxZ1pluSz8sGqdWtP73neQrWJOBJou1/DxEKDD+CUlStuReXQHle+wibeJdClR+aWxWX7gAOEcdflxy2E3aGj9S/9J4ILnEK/5pnvLyG26QDLS6qjfwMbzbCYvrFn5VTS1GHLVUZsncF52GxVlBNN0vyEsXUy2PfZgRUz8O3de4R9j20zVEZMgNeov4JRNPjAxNohoulS72WA2uFen124S7mO0Z2TQMIhC31v6QdhbXinQsNE3fXfqxEME/7D5kAvLt+pWxZYrQpmQAhOpqApo9Y1YFUK78qddY64HCRrbRJg30lG6vyUYj6QUGVsH1Sjj3q7p+6mZCq/yde9fwk0PmTU9Zi3vi+B8fCT373PmJ28yWjql8LHBxpPhoLTx/RIQDP1Rv/Oh/5ORxOfteNZit+fTX9FNSkZZEM6E85xNcxejDGIMktyJY8Bp/OrTJmG+01IAC/s9n8Ox1qqlccodaSmeLaHx0cK98k/0ZxGf/wKuiWofXXw0BcNBBDleKPhnEFcxtxlV1dXf0WflZyAVu0sMM5rQo9SozXrWTr4DX2Rt9oo/R4EG65vVcVuYA5x0I+rK04janE2v5qC/aMVX6qUfbVbVaC+JQfybmDtYtIBLmyrmnJqrUZHDW+y7PhfEysgTKD9dS9y+stuV8pyQ8pDmmfnNiPpp0eg4KC9UqFciN08Qeg4njnKB1xFx32GswLp7+k8q07MoUk6xKoUhNQBMrVE6fqSv2G6imBsScxPVaC1+cLMSzJsCntrlQO+HBx9CkOlDWZ98ZrXnjaOrVWc2i9oGKKYTTfJQ==',
    '__VIEWSTATEGENERATOR': '12999F84',
    'ctl00$ContentPlaceHolder1$UC_itm_1701$FromDate': '25.04.2015',
    'ctl00$ContentPlaceHolder1$UC_itm_1701$ToDate': '25.04.2017',
    'ctl00$ContentPlaceHolder1$UC_itm_1701$doFilterGibrid': 'Получить',
    'ctl00$ContentPlaceHolder1$UC_itm_1701$Hidden_d1': '01.01.2018',
    'ctl00$ContentPlaceHolder1$UC_itm_1701$Hidden_d2': '01.01.2015'
    }
resp = requests.post('http://www.cbr.ru/hd_base/Default.aspx?Prtid=itogidepauct', data=payload)

table = BeautifulSoup(resp.text, "lxml")

headers = [header.text for header in table.find_all('th')]

rows = []

for row in table.find_all('tr'):
    rows.append([val.text if val.text != '\n' else '' for val in row.find_all('td')])

with open('Итоги_депозитных_аукционов.tsv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(headers)
    writer.writerows(row for row in rows if row)