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

json_bufer = open(filename +".jsons","a", encoding="utf8")
print("[")
json_bufer.write("[")
for street in network:
    preparedlink = "https://nominatim.openstreetmap.org/search/?format=json&addressdetails=1&limit=10&polygon_svg=1&street="+street+"&city=Zdu%C5%84ska%20Wola"
    preparedlink = preparedlink.replace('\n','')
    r = requests.get(preparedlink)
    json_data = json.loads(r.text)
    for value in json_data:
        address_data=value["address"]
        print("{'road':'" + address_data["road"] + "','points':[")
        json_bufer.write("{'road':'" + address_data["road"] + "','points':[")
        splitted = value["svg"].split("L ")
        print(splitted)
        if len(splitted) > 1:
            splitSecondSpace=splitted[1].split(" ")
            result = [splitSecondSpace[index] + ' ' + splitSecondSpace[index+1] for index in range(len(splitSecondSpace)-1)]
            i=0
            #print("'" + splitted[0][2::][:-1] + "',")
            json_bufer.write("'" + splitted[0][2::][:-1] + "',")
            for pair in result:
                i=i+1
                if i%2==1:
                    #print ("'" + pair + "',") #tu printuje pary
                    json_bufer.write("'" + pair + "',")   
        #print("]")
        json_bufer.write("]")
        #print("},")
        json_bufer.write("},\n")
#print("]")
json_bufer.write("]")
json_bufer.close()

