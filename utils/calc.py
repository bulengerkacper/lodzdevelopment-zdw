import json

def test():
    res = {}
    
    with open('data/input.json') as src:
        data = json.load(src)

    with open('data/costs.json') as costs:
        cost = json.load(costs)

    period = float(data["period"].replace(",", "."))

    if (float(data["location"]["area"]) < 100):
        print("TODO: Dom ponizej 100m")
    
    elif (float(data["location"]["area"]) > 100 and float(data["location"]["area"]) < 200):
        house_size = 2
        print("Dom pomiedzy 100 a 200m")
 
    else:
        print("TODO: Dom pomiedzy 100 a 200m")
        
    res_gas = calc(house_size, cost, "gas", period)
    res_network = calc(house_size, cost, "urban_network", period)
    res_electricity = calc(house_size, cost, "electricity", period)

    res["gas"] = res_gas
    res["urban_network"] = res_network
    res["electricity"] = res_electricity

    return pack_data(res, period)



def calc(size, costs, medium, period):
    result = []
    
    result_installation = 0
    if (size == 1):
        print("TODO")
    elif (size == 2):
        for x in costs[medium]["installation"]:
            result_installation += float(costs[medium]["installation"][x].replace(",", ".")) #TODO: refactor
    else: 
        print("TODO")

    results_exploatation = float(costs[medium]["exploatation"]["fixed_200"].replace(",", ".")) * period

    result.append(result_installation)
    result.append(results_exploatation)

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