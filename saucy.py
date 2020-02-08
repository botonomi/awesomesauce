from bs4 import BeautifulSoup
from multiprocessing import Pool
import os
import re
import requests
import whisper
import base64

import sys

suspect = 'https://github.com/lbonanomi/the-book-of-secret-knowledge/blob/master/README.md'

bulk = requests.get(suspect)
soup = BeautifulSoup(bulk.text, 'html.parser')

whisper_db_dir = os.getenv("HOME") + '/whispers/'

#RETAINER = [(259200, 6)]                      # [(seconds_in_period, slots_in_period)]
RETAINER = [(60, 6)]

urls = {}

for wag in soup.find_all('a', attrs={'href': re.compile("^https*://")} ):
        link = wag.get('href').encode("utf-8")
        encoded = base64.b64encode(link).decode().translate(str.maketrans('/', '_'))

        urls[wag.get('href')] = encoded

def whisp(item):
        url = item[0]
        db = item[1]

        whisper_db_name = whisper_db_dir + db + '.wsp'

        if not os.path.exists(whisper_db_name):
                whisper.create(whisper_db_name, RETAINER, aggregationMethod='last')

        try:
                code = requests.get(url).status_code
        except Exception:
                code = 500

        try:
                whisper.update(whisper_db_name, code)
        except Exception:
                print("Can't update DB for ", url, "?")

        (times, fails) = whisper.fetch(whisper_db_name, 315550800)

        x = 0

        for spot in fails:
                try:
                        x = x + spot
                except TypeError:
                        continue

        if x > 1200:
                print(url + ":" + str(int(fails.pop())))


p = Pool(10)
p.map(whisp, urls.items())
