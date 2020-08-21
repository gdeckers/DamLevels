from django.contrib import admin
from django.contrib.gis.geos import Point
from datetime import datetime
from leaflet.admin import LeafletGeoAdmin
import pandas as pd
import requests
from damlevelsapp.models import DamLevels
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# Register your models here.
class DamLevelsAdmin(LeafletGeoAdmin):
    pass

admin.site.register(DamLevels, DamLevelsAdmin)

options = Options()
options.headless = True

driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.PhantomJS()
url = "http://www.capetown.gov.za/Family%20and%20home/residential-utility-services/residential-water-and-sanitation-services/this-weeks-dam-levels"
driver.get(url)
time.sleep(2)

#dados = driver.find_element_by_class_name("mobile-scroll")

dado = driver.find_element_by_id("Heading1")  #tabela css:4746
#print(dado)

html = dado.get_attribute("innerHTML")
#print(html)

soup = BeautifulSoup(html, "html.parser")

table = soup.select_one("table")
#print(table)

driver.close()

line = []
row_list = []

data = [d for d in table.select("tr")]
#print(data)

for tr in data:
    td = tr.find_all('td')
    th = tr.find_all('th')
    row = [tr.text.strip() for tr in td if tr.text.strip()]
    head = [tr.text.strip() for tr in th if tr.text.strip()]
    #print(head)


    if head:
 #       print(head)
        head[0] = 'Dam'
 #       print(head)
#        head[1]='Dam'
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

for index, row in df_damData.iterrows():
    Id = index
    Dam = row[0]
    ThisWeek = row[1]
    LastWeek = row[2]
    LastYear = row[3]
    CreationDate = datetime.now()
    Latitude = row[4]
    Longitude = row[5]

    DamLevels(Id=Id, Dam=Dam, ThisWeek=ThisWeek, LastWeek=LastWeek, LastYear=LastYear, CreationDate=CreationDate,
              geom=Point(Longitude, Latitude)).save()



