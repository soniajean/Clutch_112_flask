import requests as r


def roundDrivers(round):
    d_list = []
    x = r.get(f"http://ergast.com/api/f1/2010/{round}/drivers.json")
    d = x.json()
    y = d['MRData']['DriverTable']['Drivers']
    for a in y:
        d_list.append(a['driverId'])
    return d_list



def getDriver(st):
    x = r.get(f'http://ergast.com/api/f1/drivers/{st}.json')
    d = x.json()
    # print(d)
    driver = {}
    first_name = d['MRData']['DriverTable']['Drivers'][0]['givenName']
    last_name = d['MRData']['DriverTable']['Drivers'][0]['familyName']
    nation = d['MRData']['DriverTable']['Drivers'][0]['nationality']
    driver['id'] = st
    driver['first_name'] = first_name
    driver['last_name'] = last_name
    driver['nation'] = nation
    return driver
