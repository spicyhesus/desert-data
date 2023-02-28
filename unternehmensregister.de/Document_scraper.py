import os.path
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import re
from itertools import zip_longest
df = pd.read_csv('Document_queue.csv', index_col=0)
df_document=pd.DataFrame(columns=['Company',"Information","Deletion Notice","Language","Publication"])
for row in df["Document_Links"].values :
    print(row)
    url=row
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='row back')
    dom = etree.HTML(str(soup))
    companies = dom.xpath('//div[@class="company_result"]/span/text()')
    information=dom.xpath('//div[@class="information_result"]/p/text()')
    deletion_notice=dom.xpath('//div[@class="label_result"]/div[2]/text()')
    language = dom.xpath('//div[@class="label_result"]/div[3]/text()')
    publication=dom.xpath('//div[@class="publication_container"]//text()')

    if companies is None or len(companies) == 0:
        companies = "null"
    #print(companies[0].strip())

    if information is None or len(information) == 0:
        information = "null"
    #print(information[0].strip())

    if  deletion_notice is None or len(deletion_notice) == 0:
        date = "null"
    else:
        date = re.sub(r'.', '', deletion_notice[0].strip(), count=6)
    #print(date)

    if language is None or len(language) == 0:
        lang= "null"
    else :
        lang = re.sub(r'.', '', language[0].strip(), count=10)
        lang=lang.strip()
    #print(lang)

    if publication is None or len(publication) == 0:
        pub = "null"
    else :
        stripped = [s.strip() for s in publication]

        while ("" in stripped):
            stripped.remove("")
        pub=''.join(stripped)

    df_document.loc[len(df_document.index)] = [companies[0].strip(), information[0].strip(), date, lang,pub]

if os.path.exists("Documents.xlsx") :
    os.remove("Documents.xlsx")
    df_document.to_excel("Documents.xlsx")
else :
    df_document.to_excel("Documents.xlsx")