import requests

with open('siec_gazowa.txt', encoding="utf8") as f:
    lines = f.readlines()

network=[]
for line in lines:
    network.append(line)

for street in network:
    #print(street)
    preparedlink = "https://nominatim.openstreetmap.org/search/"+street +"%20Zdu%C5%84ska%20Wola?format=json&addressdetails=1&limit=1&polygon_svg=1"
    print(preparedlink)
    #r = requests.get("https://nominatim.openstreetmap.org/search/" + street + "%20Zdu%C5%84ska%20Wola?format=json&addressdetails=1&limit=1&polygon_svg=1")




