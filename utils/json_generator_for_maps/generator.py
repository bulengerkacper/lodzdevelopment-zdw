import requests
import json
import time

with open('siec_gazowa.txt', encoding="utf8") as f:
    lines = f.readlines()

network=[]
for line in lines:
    network.append(line)

for street in network:
    preparedlink = "https://nominatim.openstreetmap.org/search/"+street+"%20Zdu%C5%84ska%20Wola?format=json&addressdetails=1&limit=1&polygon_svg=1"
    preparedlink = preparedlink.replace('\n','')
    r = requests.get(preparedlink)
    data = json.loads(r.text)
    for x in data:
        #print(x["svg"])
        print (x["address"])
        # data2=json.loads(x["address"].dump())
        # for z in data2:
        #     print(z["roads"])
        
