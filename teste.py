import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.headless = True

driver = webdriver.Chrome(chrome_options=options) #Safari()
#driver = webdriver.PhantomJS()
url = "http://www.capetown.gov.za/Family%20and%20home/residential-utility-services/residential-water-and-sanitation-services/this-weeks-dam-levels"
#url = 'http://www.capetown.gov.za/Family%20and%20home/residential-utility-services/residential-water-and-sanitation-services/this-weeks-dam-levels#Heading1.html'

driver.get(url)

time.sleep(8)

dados = driver.find_element_by_class_name("mobile-scroll")

dado = driver.find_element_by_id("Heading1")  #tabela css:4746
#print(dado)

html = dado.get_attribute("innerHTML")#("innerHTML")
#print(html)


soup = BeautifulSoup(html, "html.parser")

table = soup.select_one("table")
#print(table)

line = []
# data = [d for d in table.select("tr")]
# for d in data:
#     linha = ""
#     for t in d.select("td"):
#         linha += t.text+","
#     line.append(linha)
driver.close()

data = [d for d in table.select("tr")]
#print(data)
row_list = []

for tr in data:
    td = tr.find_all('td')
    th = tr.find_all('th')
    row = [tr.text.strip() for tr in td if tr.text.strip()]
    head = [tr.text.strip() for tr in th if tr.text.strip()]
    #print(head)

    if head:
        head[0] = 'Dam'
        row_list.append(head)
    if row:
        row_list.append(row)

#print(row_list)
row_list_no_totals = row_list[1:-2]
#print(row_list_no_totals)
row_list_no_totals_clean = []

for r in row_list_no_totals:
    #print(r)
    row_list_no_totals_clean.append([s.replace('#','') for s in r])

df = pd.DataFrame(row_list_no_totals_clean, columns=row_list[0], dtype=float)

df_location = pd.read_csv('damLocations.txt', delimiter=',')

df_damData = df.merge(df_location, how='left')
#print(df_damData)





