import requests
from bs4 import BeautifulSoup
from urllib import parse
import pandas as pd
import os.path
from lxml import etree

def trade_spider(max_pages):
    page=1
    df_pages=pd.DataFrame(columns=['Page_Links'])
    df_register = pd.DataFrame(columns=['Register_Links'])
    df_deposit_tree = pd.DataFrame(columns=['Deposit_tree_Links'])
    df_document = pd.DataFrame(columns=['Document_Links'])
    while page <=max_pages :
        url="https://www.unternehmensregister.de/ureg/result.html;jsessionid=F3F0340FF146154A211EBDCBB798DD9E.web03-1?submitaction=pathnav&page."+str(page)+"=page"
        print(url)
        df_pages.loc[len(df_register)] = url
        source_code= requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        for data in soup.findAll('div', attrs={'class': 'container result_container global-search'}):
                links= data.findAll('a')
                for a in links :
                    embeded_url=parse.urljoin("https://www.unternehmensregister.de/ureg/result.html;jsessionid=F3F0340FF146154A211EBDCBB798DD9E.web03-1?submitaction"
                                              ,a['href'])
                    if "registerPortalAdvice" in embeded_url :
                        df_register.loc[len(df_register)] = embeded_url
                    elif "showDepositTree" in embeded_url :
                        #print(embeded_url)
                        df_deposit_tree.loc[len(df_deposit_tree)] = embeded_url
                    elif "showDocument" in embeded_url:
                       # print(embeded_url)
                        df_document.loc[len(df_document)] = embeded_url
        page +=1

    if os.path.exists("Pages_queue.csv") :
        os.remove("Pages_queue.csv")
        df_pages.to_csv("Pages_queue.csv")
    else :
        df_pages.to_csv("Pages_queue.csv")

    if os.path.exists("Register_queue.csv") :
        os.remove("Register_queue.csv")
        df_register.to_csv("Register_queue.csv")
    else :
        df_register.to_csv("Register_queue.csv")

    if os.path.exists("Deposit_tree_queue.csv") :
        os.remove("Deposit_tree_queue.csv")
        df_deposit_tree.to_csv("Deposit_tree_queue.csv")
    else :
        df_deposit_tree.to_csv("Deposit_tree_queue.csv")

    if os.path.exists("Document_queue.csv"):
        os.remove("Document_queue.csv")
        df_document.to_csv("Document_queue.csv")
    else:
        df_document.to_csv("Document_queue.csv")

url="https://www.bundesanzeiger.de/pub/de/suchen2?35"
source_code= requests.get(url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text,"html.parser")
dom = etree.HTML(str(soup))
#pages = dom.xpath('//*[@id="content"]/section[2]/div/div/div/div/div[5]/div[1]/span/text()')
pages = soup.find('div',attrs={'class': 'page_count'}).getText()
print(pages)
res=[int(s) for s in pages.split() if s.isdigit()]
print(res[0])
#trade_spider(1)