#Aim: scraping a list of the most populous incorporated places of the United States from google
import pandas as pd
from bs4 import BeautifulSoup

#clean raw data scrapped from website
def clean_str(s_list):
    for i in range(len(s_list)):
        s_list[i] = s_list[i].strip().split('[')[0]
        s_list[i] = s_list[i].strip().split('(')[0]
    return s_list
def deal_location(raw_list):
    for item in raw_list:
        item[-1] = item[-1].replace('\ufeff','').split(' / ')[1]
    return raw_list

#get cities data from google
f = open('cities.html', 'r', encoding='utf-8')
html_text = f.read()
soup = BeautifulSoup(html_text, 'html.parser')
cities_table = soup.find('table',class_="wikitable sortable jquery-tablesorter")

headrow = cities_table.find('tr')
col_names = [th.text.strip() for th in headrow.find_all('th')]
rows = cities_table.find_all('tr')[1:]
col_names_new = ['City',
 'State',
 '2021estimate',
 '2020census',
 'Change',
 '2020 land area_mi',
 '2020 land area_km',
 '2020 population density_mi',
 '2020 population density_km',
 'Location']

#clean data
raw_list = []
for row in rows:
    all_cells = clean_str([c.text for c in row.find_all('td')])
    raw_list.append(all_cells)
new_raw_list = deal_location(raw_list)

#convert the data to pd.DataFrame and cached it
pd_table = pd.DataFrame(new_raw_list, columns=col_names_new)
new_pd_table = pd_table.copy(deep=True)
new_pd_table = new_pd_table.loc[:,['City','State','Location']]
new_pd_table.to_csv('cities.csv', index=False, header=True, encoding='utf-8-sig')