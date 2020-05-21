import requests
import json
import csv

url = requests.get('https://dev.to/api/articles?top=50')

r = url.json()

for i in range(30):
    a = r[i].get('user')
    print(a)


#data = json.loads(r)


#for s in r['user']:
#   print(s['name'])
#assert  url.status_code == 200

#print(r[0].get('user'))