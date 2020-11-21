import json

def test():
    res = {}
    
    with open('data/input.json') as src:
        data = json.load(src)

    with open('data/config_data.json') as new:
        config = json.load(new)

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

    # calculate costs here
    for medium in data["mediums"]:
        res[medium] = calc(heat, water, medium, period, config, size) 

    return pack_data_to_json(res, period)

def calc(heat, water, medium, period, config, size):
    result               = []
    
    # TODO: sprawnosc kotla ???!!!
    
    # heating
    heating                 = heat / float(config["heating_type"][medium]["heating_value"].replace(",", "."))
    heating_cost            = heating * float(config["heating_type"][medium]["price"].replace(",", "."))
    result_installation = 0
    result_exploatation = 0
    
    # water heating
    water_heat = water * 40.6 / 1000 / float(config["heating_type"][medium]["heating_value"].replace(",", "."))
    water_cost = water_heat * float(config["heating_type"][medium]["price"].replace(",", "."))

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
        print("ERROR: Wrong config for medium: " + str(medium) + "  field: " + str(x) + "  errmsg: " + str(e))
        result_installation = 0
    
    result.append(result_installation)
    result.append(result_exploatation)

    return(result)


def pack_data_to_json(results, period):
    data = {}
    for x in results:
        data[x] = {
            "installation": results[x][0],
            "exploatation": results[x][1],
            "total": results[x][0] + results[x][1],
            "period": period
        }

    y = json.dumps(data)
    return(y)