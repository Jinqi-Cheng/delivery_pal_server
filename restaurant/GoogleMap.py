"""
Create Date , 
@author: 
"""
import json
import urllib.request
from itertools import permutations
from collections import defaultdict
import math
import numpy as np
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
        if "（" in url or "，" in url or "ﬂ" in url or "#" in url:
        # if "（" in url or "，" in url:
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
            print(get_zipcode(data))
            res.append([data["results"][0]["geometry"]["location"]['lat'],
                        data["results"][0]["geometry"]["location"]['lng']])
    return res,good_addr,err
def addr_to_zipcode(addr_list):
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
        if "（" in url or "，" in url or "ﬂ" in url or "#" in url:
        # if "（" in url or "，" in url:
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
            res.append(get_zipcode(data))
    return res,good_addr,err
def get_zipcode(data):
    items = data["results"][0]["address_components"]
    zipcode = None
    for item in items:
        if item['types'][0] == "postal_code":
            zipcode = item["short_name"]
    return zipcode
def distance_matrix(addr_list,addr_list2=None):
    if not addr_list2:
        assert len(addr_list) <= 10
        addresses = [addr.replace(" ", "+") for addr in addr_list]
        addr_str = "|".join(addresses)
        api_key = "AIzaSyB6qF6LxDz2bo1cY0A_yqVAvjl1wGk20Ls"
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}".format(
            addr_str, addr_str, api_key)
    else:
        assert len(addr_list) <= 10
        print(addr_list)
        assert len(addr_list2) <= 10
        addresses = [addr.replace(" ", "+") for addr in addr_list]
        addresses2 = [addr.replace(" ", "+") for addr in addr_list2]
        addr_str = "|".join(addresses)
        addr_str2 = "|".join(addresses2)
        api_key = "AIzaSyB6qF6LxDz2bo1cY0A_yqVAvjl1wGk20Ls"
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}".format(
            addr_str, addr_str2, api_key)
    print(url)
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
def large_distance_matrix(addr_list):
    n = len(addr_list)
    matrix = np.zeros((n,n))
    n_block = math.ceil(n/10)
    if(n<=10):
        return distance_matrix(addr_list)
    else:
        for i in range(n_block):
            for j in range(n_block):
                matrix[i*10:(i+1)*10,j*10:(j+1)*10] = np.asarray(distance_matrix(addr_list[i*10:(i+1)*10],addr_list[j*10:(j+1)*10]))
        return matrix.tolist()
def large_distance_matrix_restaurant(addr_list,restaurant_addr):
    n = len(addr_list)
    matrix = np.zeros((1,n))
    n_block = math.ceil(n/10)
    if(n<=10):
        return distance_matrix([restaurant_addr],addr_list)
    else:
        for i in range(1):
            for j in range(n_block):
                mat = np.asarray(distance_matrix([restaurant_addr],addr_list[j*10:(j+1)*10]))
                print(mat)
                matrix[i*10:(i+1)*10,j*10:(j+1)*10] = mat
        return matrix.tolist()
def position_dict(addr_list):
    positions,good_addr,err = geocode(addr_list)
    dic = dict()
    for index1,point1 in enumerate(positions):
        for index2,point2 in enumerate(positions):
            dic[(index1,index2)] = math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    return dic
def position_dict_with_restaurant_address(addr_list,restaurant_address):
    positions,good_addr,err = geocode(addr_list)
    restaurant_positions,_,_ = geocode([restaurant_address])
    restaurant_positions = restaurant_positions[0]
    dic = dict()
    for index1,point1 in enumerate(positions):
        for index2,point2 in enumerate(positions):
            dic[(index1,index2)] = math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
        dic[(-1,index1)] = math.sqrt((point1[0]-restaurant_positions[0])**2+(point1[1]-restaurant_positions[1])**2)
    return dic

def position_dict_with_restaurant_address_by_drive_route(addr_list,restaurant_address):
    matrix = large_distance_matrix(addr_list)
    restaurant_mat = large_distance_matrix_restaurant(addr_list,restaurant_address)
    n = len(matrix)
    dic = dict()
    for index1 in range(n):
        for index2 in range(n):
            dic[(index1, index2)] = matrix[index1][index2]
        dic[(-1, index1)] = restaurant_mat[0][index1]
    return dic