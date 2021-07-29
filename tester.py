import requests
import json

zipcode = 15217
URL = "http://flip3.engr.oregonstate.edu:59001/both"

location = "736 Saddle Horn Trail, Vacaville, CA"

PARAMS = {'address':location}

r = requests.get(url = URL, params = PARAMS)

link = r.json()

#link = json_r['link_to']
print(link)