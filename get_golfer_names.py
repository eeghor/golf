"""
collect golfer name list from wikipedia
"""

import requests
from bs4 import BeautifulSoup
import sys
from unidecode import unidecode
import os
from datetime import datetime

GOLFER_GENDER = 'female'  # choose 'male' or 'female'
assert GOLFER_GENDER in "male female".split(), print('golfer gender must be either male or female..')

BASE_URL = 'https://en.wikipedia.org/wiki/List_of_' + GOLFER_GENDER + '_golfers'
DATA_DIR = 'data'

golfers = set()

try:
	os.mkdir(DATA_DIR)
except FileExistsError:
	print("data directory {} already exists".format(DATA_DIR.upper()))

soup = BeautifulSoup(requests.get(BASE_URL).text, 'html.parser')

# find what letters are available
try:
	content_tbl = soup.find('table', id='toc', summary='Contents')
except:
	print('can\'t find the content table! quitting..')
	sys.exit(0)

letters = [a.get('href')[-1] for a in content_tbl.find_all('a') if len(a.get('href')) == 2]

# for each letter, find the corresponding section
for letter in letters:
	table = soup.find('span', class_='mw-headline', id=letter).parent.next_sibling.next_sibling
	for td in table.find_all('td'):
		try:
			flag = td.find_all('span', class_='flagicon')[-1]
			player = ' '.join([w for w in unidecode(flag.next_sibling.next_sibling.get('title')).strip().lower().split() 
					if w and (w.isalpha() or '-' in w)  and (len(w) > 1) and w != 'hof'])
			golfers.add(player)
		except:
			# it's an entry containing years, ignore
			pass

print('found {} {} golfers'.format(len(golfers), GOLFER_GENDER))
print('saving name list to file...', end='')
# save the players to a file
right_now = datetime.now()
tm_stamp = "{:02d}{:02d}{:02d}".format(right_now.day, right_now.month, right_now.year)
with open(DATA_DIR + '/' + "-".join(['golfers', GOLFER_GENDER, tm_stamp]) + ".txt", 'w') as f:
	for golfer in golfers:
		f.write('{}\n'.format(golfer))
print('ok')

		

