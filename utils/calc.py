import json

def test():
    with open('data/input.json') as src:
        data = json.load(src)

    with open('data/costs.json') as costs:
        cost = json.load(costs)

    period = float(data["period"].replace(",", "."))

    if (float(data["location"]["area"]) < 100):
        print("Dom ponizej 100m")
    
    elif (float(data["location"]["area"]) > 100 and float(data["location"]["area"]) < 200):
        print("Dom pomiedzy 100 a 200m")
        res = calc(2, cost, "gas", period)
        

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

    x = {
        "installation": results[0],
        "exploatation": results[1],
        "total": results[0] + results[1],
        "period": period
    }

    y = json.dumps(x)
    return(y) 