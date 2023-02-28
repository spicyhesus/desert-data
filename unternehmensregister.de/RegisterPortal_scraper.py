import os.path
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
from urllib import parse
from itertools import zip_longest

df = pd.read_csv('Register_queue.csv', index_col=0)
df_register=pd.DataFrame(columns=['Company','Land','Register Office','History','History Status'])
print(df_register)
for row in df["Register_Links"].values :
    #print(row)
    url=row
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))
    button=dom.xpath('//div[@class="btn-nav d-flex flex-row justify-content-between"]/div[@class="right"]/a/@href')
    #print(url)
    reg_url = parse.urljoin(url,button[0])
    reg_page =  requests.get(reg_url)
    reg_soup = BeautifulSoup(reg_page.content, 'html.parser')
    dom = etree.HTML(str(reg_soup))
    #print(url)
    land=dom.xpath('//table[@class="RegPortErg"]//tr/td[@class="RegPortErg_AZ"]/text()')
    company=dom.xpath('//table[@class="RegPortErg"]//tr/td[@class="RegPortErg_FirmaKopf"]/text()')
    register_office=dom.xpath('//table[@class="RegPortErg"]//tr/td[@class="RegPortErg_SitzStatusKopf"]/text()')
    history=dom.xpath('//table[@class="RegPortErg"]//tr[@class="RegPortErg_Klein"]/td[@class="RegPortErg_HistorieZn"][1]/text()')
    history_status=dom.xpath('//table[@class="RegPortErg"]//tr[@class="RegPortErg_Klein"]/td[@class="RegPortErg_SitzStatus"][1]/text()')
    #df_register.loc[len(df_register.index)] = [company, land, register_office, history, history_status]
    if land is None or len(land) == 0:
        land="null"

    if company is None or len(company) == 0:
        company ="null"

    if register_office is None or len(register_office) == 0:
        register_office="null"

    if history is None or len(history) == 0:
       history = "null"
    print(' '.join(history))
    if history_status is None or len(history_status) == 0:
        history_status = "null"

    df_register.loc[len(df_register.index)] = [company[0].strip(), land[0].strip(), register_office[0].strip(), ' '.join(history), ' '.join(history_status)]

if os.path.exists("Register.xlsx") :
    os.remove("Register.xlsx")
    df_register.to_excel("Register.xlsx")
else :
    df_register.to_excel("Register.xlsx")