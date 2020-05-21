"""
Create Date , 
@author: 
"""
import json
import urllib.request
from itertools import permutations
from collections import defaultdict
import math
def geocode(addr_list):
    addresses = [addr.replace(" ", "+") for addr in addr_list]
    api_key = "AIzaSyB6qF6LxDz2bo1cY0A_yqVAvjl1wGk20Ls"
    url_base = "https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}"
    lat = []
    lng = []
    res = []
    err = []
    good_addr = []
    for addr in addresses:
        url = url_base.format(api_key, addr)
        print(url)
        # if "（" in url or "，" in url or "ﬂ" in url or "#" in url:
        if "（" in url or "，" in url:
            print("url:",url)
            err.append(addr)
            continue

        data = None
        try:
            wp = urllib.request.urlopen(url)

            pw = wp.read()
            data = json.loads(pw)
        except :
            print("err: ",url)
            err.append(addr)
            continue

        # print("data:",url)
        if data['status'] != "OK":
            print("data:", url)
            print(data)
            err.append(addr)
        else:

            good_addr.append(addr)
            res.append([data["results"][0]["geometry"]["location"]['lat'],
                        data["results"][0]["geometry"]["location"]['lng']])
    return res,good_addr,err
def distance_matrix(addr_list):
    assert len(addr_list) <= 10
    addresses = [addr.replace(" ", "+") for addr in addr_list]
    addr_str = "|".join(addresses)
    api_key = "AIzaSyB6qF6LxDz2bo1cY0A_yqVAvjl1wGk20Ls"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}".format(
        addr_str, addr_str, api_key)

    wp = urllib.request.urlopen(url)

    pw = wp.read()
    data = json.loads(pw)
    matrix = []
    for row_index in range(len(data['rows'])):
        cols = data['rows'][row_index]['elements']
        matrix.append([])
        for item in cols:
            matrix[row_index].append(item['distance']['value'])
    return matrix
def position_dict(addr_list):
    positions,good_addr,err = geocode(addr_list)
    dic = dict()
    for index1,point1 in enumerate(positions):
        for index2,point2 in enumerate(positions):
            dic[(index1,index2)] = math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    return dic