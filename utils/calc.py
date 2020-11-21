import json

def test():
    res = {}
    
    with open('data/input.json') as src:
        data = json.load(src)

    with open('data/config_data.json') as new:
        config = json.load(new)

    period = float(data["period"].replace(",", "."))
    input_type = data["location"]["type"]
    heat = float(config["building_type"][input_type].replace(",", ".")) * float(data["location"]["area"].replace(",", "."))
    water = 365 * float(config["water_consumption"].replace(",", ".")) * float(data["location"]["users"].replace(",", "."))
    
    res["gas"]         = calc(heat, "gas", period, config, water)
    res["electricity"] = calc(heat, "electricity", period, config, water)

    return pack_data(res, period)
    # return "test"

def calc(heat, medium, period, config, water):
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
    for x in config["heating_type"][medium]["installation"]:
            result_installation += float(config["heating_type"][medium]["installation"][x].replace(",", ".")) #TODO: refactor
    

    result.append(result_installation)
    result.append(result_exploatation)

    return(result)


def pack_data(results, period):
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