#Aim: scraping mass shootings in the United States in 2021 from google

import pandas as pd
from bs4 import BeautifulSoup

#get table
f = open('shooting.html', 'r', encoding='utf-8')
html_text = f.read()
soup = BeautifulSoup(html_text, 'html.parser')
mass_shooting_table = soup.find('table', class_='wikitable sortable mw-datatable jquery-tablesorter')

#remove footnotes
def clean_str(s_list):
    for i in range(len(s_list)):
        s_list[i] = s_list[i].strip().split('[')[0]
        s_list[i] = s_list[i].strip().split('(')[0]
    return s_list
#change the date
def change_date(s_list):
    s_list[0] = s_list[0] + ', 2021'
    return s_list

#get headrow, columns and rows
headrow = mass_shooting_table.find('tr')
col_names = [th.text.strip() for th in headrow.find_all('th')]
rows = mass_shooting_table.find_all('tr')[1:]

#clean data
raw_list = []
for row in rows:
    all_cells = clean_str([c.text for c in row.find_all('td')])
    change_date(all_cells)
    raw_list.append(all_cells)

#convert the data to pd.DataFrame and cached it
pd_table = pd.DataFrame(raw_list, columns=[col_names])
pd_table.rename(columns={'2021 date': 'date'}, inplace=True)
pd_table.to_csv('mass_shooting.csv', index=False, header=True)