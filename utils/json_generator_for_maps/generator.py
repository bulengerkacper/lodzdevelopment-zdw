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
    f = open("siec.txt","w", encoding="utf8")
    f.write("Now the file has more content!")
    for value in data:
        #print(value["svg"])
        data2=value["address"]
        #print(data2["road"])
        f.write(data2["road"])
        f.write("\n")
        f.write(value["svg"])
        f.write("\n")
    f.close()


