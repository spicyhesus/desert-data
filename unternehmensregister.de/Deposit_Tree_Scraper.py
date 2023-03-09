import os.path
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import re
from itertools import zip_longest
df = pd.read_csv('Deposit_tree_queue.csv', index_col=0)
df_deposit_tree=pd.DataFrame(columns=['Company',"District Court","Registration Number","Number Of Documents"])
for row in df["Deposit_tree_Links"].values :
    print(row)
    url=row
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='row back')
    dom = etree.HTML(str(soup))
    company=dom.xpath("//*[@id='content']/section[2]/div/div/div/div/h2/text()")
    district_court=dom.xpath("//*[@id='content']/section[2]/div/div/div/div/h2/span/text()")
    year = dom.xpath("//*[@class='year_result']/a/text()")
    if company is None :
        company="null"
    else:
        company = re.sub(r'.', '', company[0].strip(), count=23)
        print(company)

    if district_court is None :
        district_court = "null"
        reg_number = "null"
    else :

        district_court = re.sub(r'.', '', district_court[0].strip(), count=15)
        print(district_court)

        district = re.search('([^\s]+)', district_court)
        if district is None :
            district = "null"
            reg_number = "null"
        else :
            district = district.group(1).strip()
            reg_number = re.sub(r'.', '', district_court, count=len(district) + 1)
        print(district)
        print(reg_number)

    if year is None :
        year=0
    else :
        year =len(year)
        print(year)

    df_deposit_tree.loc[len(df_deposit_tree.index)] = [company, district,reg_number, year]


if os.path.exists("Deposit_tree.xlsx") :
    os.remove("Deposit_tree.xlsx")
    df_deposit_tree.to_excel("Deposit_tree.xlsx")
else :
    df_deposit_tree.to_excel("Deposit_tree.xlsx")