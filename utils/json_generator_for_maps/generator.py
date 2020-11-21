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
    preparedlink = "https://nominatim.openstreetmap.org/search/?format=json&addressdetails=1&limit=1&polygon_svg=1&street="+street+"&city=Zdu%C5%84ska%20Wola"
    preparedlink = preparedlink.replace('\n','')
    r = requests.get(preparedlink)
    json_data = json.loads(r.text)
    f = open(filename +".json","a", encoding="utf8")
    for value in json_data:
        address_data=value["address"]
        f.write(address_data["road"])
        f.write("\n")
        #f.write(value["svg"]) //cala wartosc ml
        splitted = value["svg"].split("L ",1)
        #f.write(splitted[1]) #tu printuje cala zawartosc bez l
        splitSecondSpace=splitted[1].split(" ")
        result = [splitSecondSpace[index] + ' ' + splitSecondSpace[index+1] for index in range(len(splitSecondSpace)-1)]
        i=0
        for pair in result:
            i=i+1
            if i%2==1:
                print (pair) #tu printuje pary
                f.write(pair)
                f.write("\n")
        f.write("\n")
    f.close()


