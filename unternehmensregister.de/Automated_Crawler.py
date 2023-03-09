from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
from urllib import parse
import pandas as pd
import os.path
from lxml import etree

df_pages = pd.DataFrame(columns=['Page_Links'])
df_register = pd.DataFrame(columns=['Register_Links'])
df_deposit_tree = pd.DataFrame(columns=['Deposit_tree_Links'])
df_document = pd.DataFrame(columns=['Document_Links'])

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

driver.get('https://www.unternehmensregister.de/ureg/?submitaction=language&language=en')

# Wait for cookie popup to appear
wait = WebDriverWait(driver, 5)
cookie_popup = wait.until(EC.visibility_of_element_located((By.ID, "cc_banner")))

# Click "Accept All Cookies" button
accept_button = wait.until(EC.element_to_be_clickable((By.ID, "cc_all")))
accept_button.click()
# Wait for the extended search button to appear and click it
extended_search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="globalSearchForm"]/div[3]/div[1]/p/a/button')))
extended_search_button.click()

# Wait for the date fields to appear and enter start and end dates
start_date_field = wait.until(EC.visibility_of_element_located((By.ID, "searchRegisterForm:extendedResearchStartDate")))
end_date_field = wait.until(EC.visibility_of_element_located((By.ID, "searchRegisterForm:extendedResearchEndDate")))
driver.execute_script("arguments[0].value = '03/9/2023'", start_date_field)
driver.execute_script("arguments[0].value = '03/9/2023'", end_date_field)
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchRegisterForm"]/div[12]/input[2]')))
search_button.click()


#language_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='?submitaction=language&amp;language=en']")))
#language_button.click()
#driver.execute_script("arguments[0].value = 'EN'", language_button)
#time.sleep(60)
while True:
    #links = driver.execute_script(
    #    "return Array.from(document.querySelectorAll('div.result_pager div.pagination div.right div.next a')).map(a => a.href)")
    #for link in links:
     #   print(link)
    current_url = driver.current_url
    url = current_url
    print(url)
    df_pages.loc[len(df_register)] = url
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for data in soup.findAll('div', attrs={'class': 'container result_container global-search'}):
        links = data.findAll('a')
        for a in links:
            embeded_url = parse.urljoin(
               url, a['href'])
            print(embeded_url)
            if "registerPortalAdvice" in embeded_url:
                df_register.loc[len(df_register)] = embeded_url
            elif "showDepositTree" in embeded_url:
                # print(embeded_url)
                df_deposit_tree.loc[len(df_deposit_tree)] = embeded_url
            elif "showDocument" in embeded_url:
                # print(embeded_url)
                df_document.loc[len(df_document)] = embeded_url
    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.pagination div.right div.next a')))
    next_button_link = next_button.get_attribute('href')
    if not next_button_link:
        break
    #print(next_button_link)
    next_button.click()

    #else:
    #    next_button.click()


if os.path.exists("Pages_queue.csv"):
    os.remove("Pages_queue.csv")
    df_pages.to_csv("Pages_queue.csv")
else:
    df_pages.to_csv("Pages_queue.csv")

if os.path.exists("Register_queue.csv"):
    os.remove("Register_queue.csv")
    df_register.to_csv("Register_queue.csv")
else:
    df_register.to_csv("Register_queue.csv")

if os.path.exists("Deposit_tree_queue.csv"):
    os.remove("Deposit_tree_queue.csv")
    df_deposit_tree.to_csv("Deposit_tree_queue.csv")
else:
    df_deposit_tree.to_csv("Deposit_tree_queue.csv")

if os.path.exists("Document_queue.csv"):
    os.remove("Document_queue.csv")
    df_document.to_csv("Document_queue.csv")
else:
    df_document.to_csv("Document_queue.csv")


driver.quit()