"""
Create Date , 
@author: 
"""
from collections import defaultdict
from itertools import permutations
from clustering.equal_groups import EqualGroupsKMeans

from .models import Orders
from accounts.models import Restaurant
from .pdf import *
from .GoogleMap import geocode, distance_matrix, position_dict

def permutation_sort(addr_list,id_list):
    matrix = distance_matrix(addr_list)
    row = len(matrix)
    lst = permutations([i for i in range(row)])
    best_perm = None
    best_distance = float("inf")
    for perm in lst:
        curr_distance = 0
        for index in range(row - 1):
            curr_distance += matrix[perm[index]][perm[index + 1]]
        if best_distance > curr_distance:
            best_distance = curr_distance
            best_perm = perm
    print(best_perm)
    return best_perm
def insert_point(opt_seq,mat_dist,points_num):
    opt_seq = list(opt_seq)
    opt_points = set(opt_seq)
    all_points = set(range(points_num))

    remain_points = all_points-opt_points

    for point in remain_points:
        mi = float('inf')
        pos_index = -1
        for index in range(len(opt_seq)-1):
            ori_dist = mat_dist[(opt_seq[index],opt_seq[index+1])]
            new_dist1 = mat_dist[(opt_seq[index],point)]
            new_dist2 = mat_dist[(point,opt_seq[index+1])]
            if mi > new_dist1+new_dist2 - ori_dist:
                mi = new_dist1+new_dist2 - ori_dist
                pos_index = index+1
        if mi > mat_dist[(opt_seq[0],point)]:
            mi = mat_dist[(opt_seq[0],point)]
            pos_index = 0
        if mi > mat_dist[(opt_seq[-1],point)]:
            mi = mat_dist[(opt_seq[-1],point)]
            pos_index = len(opt_seq)-1
        opt_seq.insert(pos_index,point)
    return opt_seq
def insertion_permutation_sort(addr_list,id_list):
    best_seq = permutation_sort(addr_list[:10],id_list[:10])
    distance_dic = position_dict(addr_list)
    id_list = insert_point(best_seq,distance_dic,len(id_list))
    dic = dict()
    for i in range(len(id_list)):
        dic[id_list[i]] = i
    id_list = sorted(id_list, key=lambda x: dic[x])
    return id_list
class Order:

    @classmethod
    def pdf2DB(cls,file_path,restaurant_id,date):
        with open(file_path, "rb") as pdf_file:
            text = read_pdf(pdf_file)
            text = "".join(text)
            text = text.split("打印订单 - 华⼈⽣鲜第⼀站")
            text = text[1:-1]
            for txt in text:
                meals = fetch_dishes(txt)
                meals_dic = {key:value for key,value in meals}
                Orders.objects.create(idRestaurant_id=restaurant_id,
                                      idDisplay=fetch_id(txt),
                                      Price=fetch_price(txt),ReceiverName=fetch_recipient_name(txt),
                                      Meals=meals_dic,OrderDate=date,DriverId=None,Address=fetch_address(txt))
    @classmethod
    def generate_deliver_list(cls,restaurant_id, driver_id, date):
        obj = Orders.objects.filter(idRestaurant=Restaurant.objects.get(idRestaurant=restaurant_id)
                                    ,DriverId=driver_id,OrderDate=date).order_by("rank")
        print(obj,type(obj))

    @classmethod
    def parser_meals(cls, restaurant_id, date, is_lunch):
        obj = Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date).values("Meals","idDisplay")
        dic = defaultdict(list)
        for meals in obj:
            idOrder = meals['idDisplay']
            for meal,meal_num in meals['Meals'].items():
                for _ in range(int(meal_num)):
                    dic[meal].append(idOrder)
        return dic

    @classmethod
    def assign_order_driver(cls,restaurant_id,date,driver_list):
        address = Orders.objects.filter(idRestaurant_id=1,OrderDate=date).values("Address")
        address_list = [addr['Address'] for addr in address]
        position = geocode(address_list)
        cluster_model =EqualGroupsKMeans(n_clusters=len(driver_list),random_state=0)
        cluster_model.fit(position)
        for index,addr in enumerate(address_list):
            Orders.objects.filter(idRestaurant_id=restaurant_id,
                                  OrderDate=date,
                                  Address=addr).update(DriverId_id = driver_list[cluster_model.labels_[index]])

    @classmethod
    def generate_sequence(cls,restaurant_id,date):
        driver_list_query = Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date).values("DriverId_id").distinct()
        driver_list = [value['DriverId_id'] for value in driver_list_query]
        for driver in driver_list:
            order_list = Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date,DriverId_id=driver).values("Address","idDisplay")
            addr_list = []
            id_list = []
            for order in order_list:
                addr_list.append(order["Address"])
                id_list.append(order["idDisplay"])
            deliver_sequence = insertion_permutation_sort(addr_list,id_list)
            for index, order_id in enumerate(deliver_sequence):
                Orders.objects.filter(idRestaurant_id=restaurant_id,
                                      OrderDate=date,
                                      DriverId_id=driver,
                                      idDisplay=id_list[order_id]).update(Sequence=index+1)
