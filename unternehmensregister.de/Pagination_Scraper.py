import os.path
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
from itertools import zip_longest
df = pd.read_csv('Pages_queue.csv', index_col=0)
df_general=pd.DataFrame(columns=['Company',"District Court","Registration Number","Status"])
for row in df["Page_Links"].values :
    print(row)
    url=row
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='row back')
    dom = etree.HTML(str(soup))
    companies = dom.xpath('//div[@class="row back"]/div[@class="col-md-4"]/div[@class="company_result"]/span/b/text()')
    district_courts = dom.xpath('//div[@class="row back"]/div[@class="col-md-4"]/div[@class="company_result"]/p//text()[contains(., "District Court")]')
    registration_numbers = dom.xpath( '//div[@class="row back"]/div[@class="col-md-4"]/div[@class="company_result"]/p//text()[contains(., "HRA") or contains(., "HRB")]')
    company_status = dom.xpath( '//div[@class="row back"]/div[@class="col-md-4"]/div[@class="company_result"]/p//text()[contains(., "Status:")]')

    for company, court_element, registration, status in zip_longest(companies, district_courts, registration_numbers, company_status) :

        if registration is not None:
            registration = registration.strip()
        else :
            registration = "null"
        if court_element is not None:

            court = court_element.replace('District Court', '')
            court=court.strip()

        else :
            court="null"
        if status is not None :
            status=status.replace('Status:', '')
            status=status.strip()
        else :
            status = "null"
        df_general.loc[len(df_general.index)] = [company, court, registration, status]
if os.path.exists("General.xlsx") :
    os.remove("General.xlsx")
    df_general.to_excel("General.xlsx")
else :
    df_general.to_excel("General.xlsx")
