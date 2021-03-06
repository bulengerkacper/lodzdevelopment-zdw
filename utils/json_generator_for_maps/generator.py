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
json_bufer.write("[")

for street in network:
    preparedlink = "https://nominatim.openstreetmap.org/search/?format=json&addressdetails=1&limit=10&polygon_svg=1&street="+street+"&city=Zdu%C5%84ska%20Wola"
    preparedlink = preparedlink.replace('\n','')
    response = requests.get(preparedlink)
    previous_entrance=""
    json_data = json.loads(response.text)
    if response.text == "[]":
        continue
    for value in json_data:
        address_data=value["address"]
        if 'town' in address_data.keys() and address_data["town"] != "Zduńska Wola" or \
            'municipality' in address_data.keys() and address_data["municipality"] == "gmina Szadek" or \
            "Szadek" in value["display_name"] or \
            'village' in address_data.keys() and "Karsznice" in address_data["village"] or \
            'town' in address_data.keys() and address_data["town"] == "Szadek" :
            break
        if previous_entrance != address_data["road"]:
            json_bufer.write("{'road':'" + address_data["road"] + "','points':[")
        splitted = value["svg"].split("L ")
        if len(splitted) > 1:
            splitSecondSpace=splitted[1].split(" ")
            result = [splitSecondSpace[index] + ' ' + splitSecondSpace[index+1] for index in range(len(splitSecondSpace)-1)]
            i=0
            json_bufer.write("'" + splitted[0][2::][:-1] + "',")
            for pair in result:
                i=i+1
                if i%2==1:
                    json_bufer.write("'" + pair + "',")   
        previous_entrance=address_data["road"]
    json_bufer.write("]")
    json_bufer.write("},")
        
json_bufer.write("]")
json_bufer.close()

with open(filename +".jsons", "rt", encoding="utf8") as fin:
    with open(filename+".json", "wt", encoding="utf8") as fout:
        for line in fin:
            print(line)
            line=line.replace("'", '"')
            line=line.replace(",]","]")
            fout.write(line)

