"""
Create Date , 
@author: 
"""
import json
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import math
from collections import defaultdict
from itertools import permutations


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc
def analyse(df):
    # df = pd.read_csv("../../../2020送餐/daily_order2.csv")
    # print(df)
    label = []
    lat = df.lat.values.tolist()
    lng = df.lng.values.tolist()
    f = lambda x: -(x+117.2)+32.97
    for i in range(len(lat)):
        if lat[i] > f(lng[i]):
            label.append(1)
        else:
            label.append(2)
    df['label'] = label
    one_lng = df.lng[df.label==1]
    one_lat = df.lat[df.label==1]
    two_lng = df.lng[df.label==2]
    two_lat = df.lat[df.label==2]
    oid = df['id'].values.tolist()
    fig, ax = plt.subplots()
    ax.scatter(one_lng,one_lat)
    ax.scatter(two_lng,two_lat)
    lng_min = min(df.lng)
    lng_max = max(df.lng)
    line_x = [lng_min+0.001*index for index in range(int(1000*lng_max)-int(1000*lng_min))]
    # for index in range(int(100*lng_max)-int(100*lng_min)):
    #     print(index)
    line_y = [f(x) for x in line_x]

    # print(line_y)
    plt.plot(line_x,line_y)
    for i, txt in enumerate(lat):
        ax.annotate(oid[i],(lng[i],lat[i]))
    plt.show()


    print("-----------------one---------------")
    print(df.id[df.label==1].values.tolist())
    print("-----------------two---------------")
    print(df.id[df.label==2].values.tolist())
    return df

def geocode(df):
    # df = pd.read_csv("../../../2020送餐/daily_order.csv")
    # df = pd.read_csv("tmp.csv",encoding='utf-8')
    print(df.address)
    addresses = [item.replace(" ","+") for item in df.address.tolist()]
    # print(addresses)
    # print(df)
    # addr_str = "|".join(addresses)
    api_key = "AIzaSyAWMOWfy7Sxeh4Q-NV-pSEg3wPmxCQCUFQ"
    url_base = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
    lat = []
    lng = []
    for addr in addresses:
        url = url_base.format(addr,api_key)
        wp = urllib.request.urlopen(url)

        pw = wp.read()
        data = json.loads(pw)
        # print(data)
        lat.append(data["results"][0]["geometry"]["location"]['lat'])
        lng.append(data["results"][0]["geometry"]["location"]['lng'])
    plt.scatter(lng,lat)
    plt.show()
    df['lat'] = lat
    df['lng'] = lng
    # print(df)
    # df.to_csv("../../../2020送餐/daily_order2.csv")
    return df
def create_distance(df,label=1):
    # points = df[['id','lat','lng']][df.label==label].values.tolist()
    points = df[['id','lat','lng']].values.tolist()
    # print(points)
    dic = dict()
    for point1 in points:
        for point2 in points:
            dic[(int(point1[0]),int(point2[0]))] = distance_on_unit_sphere(point1[1],point1[2],point2[1],point2[2])*10000
    return dic,df['id'].values.tolist()
def create_distance_matrix(df):
    points = df[['id', 'lat', 'lng']].values.tolist()
    mat = []
    for point1 in points:
        dist_vec = []
        for point2 in points:
             dist_vec.append(distance_on_unit_sphere(point1[1], point1[2], point2[1],
                                                                            point2[2]) * 10000)
        mat.append(dist_vec)
    return mat
def generate_sequence(dic,row):
    lst = set(row)
    # seq = None
    opt_seq = None
    mi = float('inf')
    for start in lst:
        seq = [start]
        seq_dist = 0
        unvisit = lst.copy()
        unvisit.remove(start)

        while unvisit:
            # print(unvisit)
            p2p_dist = float('inf')
            next_point = None
            for point in unvisit:
                if p2p_dist> dic[(start,point)]:
                    p2p_dist = dic[(start,point)]
                    next_point = point
            seq.append(next_point)
            seq_dist+=p2p_dist
            # print(next_point)
            unvisit.remove(next_point)
            # print(seq)
        if mi > seq_dist:
            opt_seq = seq
            mi = seq_dist

    print(opt_seq)
    return opt_seq
    # print(mi)
    # print(opt_seq)
def draw_seq(df,seq):
    fig,ax = plt.subplots()
    lat = df.lat.values.tolist()
    lng = df.lng.values.tolist()
    oid = df.id.values.tolist()
    ax.scatter(lng,lat)
    for i in range(len(seq)-1):
        lat_start = float(df.lat[df.id==seq[i]])
        lat_end = float(df.lat[df.id==seq[i+1]])
        lng_start = float(df.lng[df.id==seq[i]])
        lng_end = float(df.lng[df.id==seq[i+1]])
        print([lng_start,lng_end],[lat_start,lat_end])
        ax.plot([lng_start,lng_end],[lat_start,lat_end])
    for i, txt in enumerate(lat):
        ax.annotate(oid[i],(lng[i],lat[i]))
    plt.show()
def draw_seq_index(df,seq):
    fig,ax = plt.subplots()
    lat = df.lat.values.tolist()
    lng = df.lng.values.tolist()
    oid = df.id.values.tolist()
    ax.scatter(lng,lat)
    for i in range(len(seq)-1):
        lat_start = float(df.lat[seq[i]])
        lat_end = float(df.lat[seq[i+1]])
        lng_start = float(df.lng[seq[i]])
        lng_end = float(df.lng[[i+1]])
        print([lng_start,lng_end],[lat_start,lat_end])
        ax.plot([lng_start,lng_end],[lat_start,lat_end])
    for i, txt in enumerate(lat):
        ax.annotate(oid[i],(lng[i],lat[i]))
    plt.show()
def first_ten_opt_seq(df_):
    df = df_.iloc[:10]
    addresses = [item.replace(" ", "+") for item in df.address.tolist()]
    # print(len(addresses))
    # print(addresses)
    addr_str = "|".join(addresses)
    api_key = "AIzaSyB6qF6LxDz2bo1cY0A_yqVAvjl1wGk20Ls"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}".format(
        addr_str, addr_str, api_key)
    # print(url)
    wp = urllib.request.urlopen(url)

    pw = wp.read()
    data = json.loads(pw)
    # print(data)
    mat = []
    for row_index in range(len(data['rows'])):
        cols = data['rows'][row_index]['elements']
        mat.append([])
        for item in cols:
            mat[row_index].append(item['distance']['value'])

    matrix = mat
    row = len(matrix)
    lst = permutations([i for i in range(row)])

    dic = defaultdict(int)
    for perm in lst:
        for index in range(row - 1):
            dic[perm] += matrix[perm[index]][perm[index + 1]]

    # print(list(dic.values()))
    mi = min(list(dic.values()))
    ordersequence = None
    for key, value in dic.items():
        if mi == value:
            ordersequence = key
    print(ordersequence)
    id_lst = df.id.values.tolist()
    opt_seq = [id_lst[ordersequence[i]] for i in range(len(ordersequence))]
    print(opt_seq)
    return opt_seq
def insert_point(df,opt_seq,mat_dist):
    opt_seq = list(opt_seq)
    opt_points = set(opt_seq)
    all_points = set(df.id.values.tolist())
    remain_points = all_points-opt_points
    for point in remain_points:
        mi = float('inf')
        pos_index = -1
        for index in range(len(opt_seq)-1):
            ori_dist = mat_dist[(opt_seq[index],opt_seq[index+1])]
            new_dist1 = mat_dist[(opt_seq[index],point)]
            new_dist2 = mat_dist[(point,opt_seq[index+1])]
            if mi > new_dist1+new_dist1 - ori_dist:
                mi = new_dist1+new_dist1 - ori_dist
                pos_index = index+1
        if mi > mat_dist[(opt_seq[0],point)]:
            mi = mat_dist[(opt_seq[0],point)]
            pos_index = 0
        if mi > mat_dist[(opt_seq[-1],point)]:
            mi = mat_dist[(opt_seq[-1],point)]
            pos_index = len(opt_seq)-1
        opt_seq.insert(pos_index,point)
    return opt_seq
if __name__ == '__main__':

    df = pd.read_csv("tmp.csv",encoding='utf-8')
    df = geocode(df)
    df = analyse(df)
    matrix_map = create_distance(df)
    generate_sequence(matrix_map,df.id.values.tolist())

    pass