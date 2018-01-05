'''
This program web-scrapes solar pv energy data from
the US energy information admin and shows the energy 
produced by each state in MWh in October 2017.
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series,DataFrame
import matplotlib as mpl
import matplotlib.pyplot as plt

#finds the table in the html
url = 'https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_1_17_a'
result = requests.get(url)
soup = BeautifulSoup(result.content)
tbl = soup.find('table','table')

data = []
rows = tbl.findAll('tr') #table rows
#title = soup.find('td') #title

for tr in rows:
	cols = tr.findAll('td') #data cells of the table
	
	for td in cols:
		text = td.find(text = True)
		data.append(text)	
		
state,rec_oct_data,corr_oct_data,index = [],[],[],0
regions = 'New England', 'Middle Atlantic','East North Central', 'West North Central','South Atlantic','East South Central', 'West South Central', 'Mountain','Pacific Contiguous', 'Pacific Noncontiguous','U.S. Total','NM'

#cleans up the data to remove/correct non-ints
for item in data:
	if any(char.isdigit() for char in item):
		pass
	else:
		if item not in regions:
			state.append(item)
			rec_oct_data.append(data[index+1].strip())
	index +=1

for val in rec_oct_data:
	try:
		corr_oct_data.append(int(val.replace(',','')))
	except ValueError:
		corr_oct_data.append(0)

mapped  = dict(zip(state,corr_oct_data))

fig = plt.figure()
x = list(range(len(state)))
plt.bar(x,mapped.values(),align = 'center')
plt.xticks(x,mapped.keys(),rotation = 'vertical')
fig.suptitle('State Comparison of PV Generation')
plt.xlabel('State')
plt.ylabel('GWh')
plt.margins(0)
plt.subplots_adjust(bottom = 0.25)
fig.savefig('test.jpg')
plt.show()