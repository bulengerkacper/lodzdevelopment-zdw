import requests
import json
import time
print ("Podaj nazwe pliku")
filename = input()
with open(filename, encoding="utf8") as f:
    lines = f.readlines()

network=[]
for line in lines:
    network.append(line)

for street in network:
    
    #preparedlink = "https://nominatim.openstreetmap.org/search/"+street+"%20Zdu%C5%84ska%20Wola?format=json&addressdetails=1&limit=1&polygon_svg=1"
    preparedlink = "https://nominatim.openstreetmap.org/search/?format=json&addressdetails=1&limit=1&polygon_svg=1&street="+street+"&city=Zdu%C5%84ska%20Wola"
    preparedlink = preparedlink.replace('\n','')
    r = requests.get(preparedlink)
    data = json.loads(r.text)
    f = open(filename +".json","a", encoding="utf8")
    for value in data:
        data2=value["address"]
        f.write(data2["road"])
        f.write("\n")
        #f.write(value["svg"]) //cala wartosc ml
        splitted = value["svg"].split("L ",1)
        f.write(splitted[1])
        f.write("\n")
    f.close()


