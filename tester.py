import requests
import json

zipcode = 15217
URL = "http://map-api-dan.herokuapp.com/link"

PARAMS = {'address':zipcode}

r = requests.get(url = URL, params = PARAMS)

link = r.json()

print(link)