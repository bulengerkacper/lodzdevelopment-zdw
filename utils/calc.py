import json

def do_calc(data):
    res = {}

    with open('data/config_data.json') as new:
        config = json.load(new)
    print(data)
    print("-----------")
    # prepare data for calculation
    period = float(data["period"].replace(",", "."))
    building_type = data["location"]["type"]
    area = float(data["location"]["area"].replace(",", "."))
    size = 0

    if area < 100:
        size = 1
    elif area >= 100 and area < 200:
        size = 2
    else:
        size = 3

    heat = float(config["building_type"][building_type].replace(",", ".")) * area
    water = 365 * float(config["water_consumption"].replace(",", ".")) * float(data["location"]["users"].replace(",", "."))

    

    # calculate referral value
    heat_ref = (heat * 100) / 60
    water_ref = (water * 100) / 60

    test = calc(heat, water, "gas", 1, config, size)   
    ref = calc(heat_ref, water_ref, "coal", 1, config, size)   

    # calculate costs here
    for medium in data["mediums"]:
        calcs = {}
        
        for period in range(0,22,2):
            result = calc(heat, water, medium, period, config, size) 
            if result != -1:
                calcs[period] = result
        
        res[medium] = calcs
    return pack_data_to_json(res, period)

def calc(heat, water, medium, period, config, size):
    
    result = []
    result_installation = 0
    result_exploatation = 0
    # TODO: sprawnosc kotla ???!!!
    try:
        # heating
        heating                 = heat / float(config["heating_type"][medium]["heating_value"].replace(",", "."))
        heating_cost            = heating * float(config["heating_type"][medium]["price"].replace(",", "."))

        # water heating
        water_heat = water * 40.6 / 1000 / float(config["heating_type"][medium]["heating_value"].replace(",", "."))
        water_cost = water_heat * float(config["heating_type"][medium]["price"].replace(",", "."))
    except Exception as e:
        print("ERROR: Error during calculation. errmsg: " + str(e))
        return -1

    result_exploatation = (heating_cost + water_cost) * period

    # installation cost
    try:
        for x in config["heating_type"][medium]["installation"]:
 
            if x == "inside_100" and size != 1:
                continue
            if x == "inside_200" and size != 2:
                continue
            if x == "inside_200+" and size != 3:
                continue
            
            result_installation += float(config["heating_type"][medium]["installation"][x].replace(",", ".")) #TODO: refactor
    
    except Exception as e:
        print("ERROR: Wrong config for medium: " + str(medium) + "  errmsg: " + str(e))
        result_installation = 0
    
    result.append(result_installation)
    result.append(result_exploatation)

    return(result)


def pack_data_to_json(results, period):
    data = {}
    tempdict = {}
    for medium in results:
        lista = []
        tempdict = {}
        for period in results[medium]:
            tempdict[period] = { 
                    "installation": results[medium][period][0],
                    "exploatation": results[medium][period][1],
                    "total": results[medium][period][0] + results[medium][period][1]
                }
        lista.append(tempdict)
        data[medium] = lista
    z = json.dumps(data)
    return z
