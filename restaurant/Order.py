"""
Create Date ,
@author:
"""
from collections import defaultdict
from itertools import permutations
from clustering.equal_groups import EqualGroupsKMeans
import re
from django.db.models import F, Max
import pandas as pd

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
    def CSV2DB(cls,df,restaurant_id,date):
        Orders.objects.filter(idRestaurant_id=restaurant_id, OrderDate=date).delete()

        length = len(df)
        for row_index in range(length):
            row = df.iloc[row_index]
            id_display = row.订单序号
            is_pickup = False
            if "送货地址" in df.columns:
                if row.送货地址 == "nan":
                    is_pickup = True
                    address = row.提货点 if "提货点" in df.columns and row.提货点 != "nan" else ""
                else:
                    is_pickup = False
                    address = row.送货地址
            address = address.replace("\n", "")
            phone = row.手机号码
            name = row.客户昵称
            note = row.备注 if "备注" in df.columns and row.备注 != "nan" else ""
            price = row.现金支付金额
            meals = re.findall(re.compile(r"(.*) \* (\d*)", re.M), row.商品汇总)
            meals_dic = {key: value for key, value in meals}
            Orders.objects.create(idRestaurant_id=restaurant_id,
                                  idDisplay=id_display,
                                  Price=price, ReceiverName=name,
                                  Meals=meals_dic, OrderDate=date, DriverId=None, Address=address,
                                  isPickup=is_pickup,
                                  Phone=phone,
                                  Note=note)
        pass
    @classmethod
    def shopify_CSV2DB(cls,df):
        length = len(df)
        dic = dict()
        if 'Shipping Name' in df.columns:
            df['Shipping Name'] = df['Shipping Name'].astype(str)
        if 'Phone' in df.columns:
            df['Phone'] = df['Phone'].astype(str)
        if 'Notes' in df.columns:
            df['Notes'] = df['Notes'].astype(str)
        if 'Shipping Address1' in df.columns:
            df['Shipping Address1'] = df['Shipping Address1'].astype(str)
        if 'Shipping Address2' in df.columns:
            df['Shipping Address2'] = df['Shipping Address2'].astype(str)
        if 'Name' in df.columns:
            df['Name'] = df['Name'].astype(str)
        if 'Lineitem name' in df.columns:
            df['Lineitem name'] = df['Lineitem name'].astype(str)
        if 'Lineitem quantity' in df.columns:
            df['Lineitem quantity'] = df['Lineitem quantity'].astype(str)
        for row_index in range(length):
            row = df.iloc[row_index]
            if row['Name'] not in dic:
                order_dic = dict()
                order_dic['客户昵称'] = row['Shipping Name']
                order_dic['手机号码'] = str(round(float(row['Phone']))) if row['Phone'] != "nan" else ""
                order_dic['备注'] = row['Notes'] if row['Notes'] != "nan" else ""
                order_dic['送货地址'] = (row['Shipping Address1'] if row['Shipping Address1'] != "nan" else "") + \
                                    " " + \
                                    (row['Shipping Address2'] if row['Shipping Address2'] != "nan" else "")
                order_dic['现金支付金额'] = 0
                order_dic['提货点'] = ""
                order_dic['订单序号'] = row['Name'][1:]  # remove the first pound
                order_dic['商品汇总'] = row['Lineitem name'] + \
                                    " * " + \
                                    row['Lineitem quantity']
                dic[row['Name']] = order_dic
            else:
                dic[row['Name']]['商品汇总'] += "\n" + row['Lineitem name'] + " * " + row['Lineitem quantity']
        df = pd.DataFrame(columns=['客户昵称', '手机号码', '备注', '送货地址', '现金支付金额', '提货点', '订单序号', '商品汇总'])
        for value in dic.values():
            df = df.append([value], ignore_index=True)
        return df
    @classmethod
    def Weee_excel_preprocess(cls, df):
        if "送货地址" in df.columns:
            df['送货地址'] = df['送货地址'].astype(str)
        if "提货点" in df.columns:
            df['提货点'] = df['提货点'].astype(str)
        if "现金支付金额" in df.columns:
            df['现金支付金额'] = df['现金支付金额'].astype(float)
        if "备注" in df.columns:
            df["备注"] = df["备注"].astype(str)
        if "商品汇总" in df.columns:
            df["商品汇总"] = df["商品汇总"].astype(str)
        return df

    @classmethod
    def Weee_CSV_preprocess(cls, df):
        if "送货地址" in df.columns:
            df['送货地址'] = df['送货地址'].astype(str)
        if "提货点" in df.columns:
            df['提货点'] = df['提货点'].astype(str)
        if "现金支付金额" in df.columns:
            df['现金支付金额'] = df['现金支付金额'].astype(float)
        if "备注" in df.columns:
            df["备注"] = df["备注"].astype(str)
        df["商品汇总"] = df[df.columns[-1]]
        if "商品汇总" in df.columns:
            df["商品汇总"] = df["商品汇总"].astype(str)
        return df


    @classmethod
    def csv2DB_check(cls, file_path, restaurant_id, date, is_lunch):
        date += " 12:00" if is_lunch else " 18:00"
        df = pd.read_csv(file_path)
        if "商品汇总" not in df.columns:
            df = Order.shopify_CSV2DB(df)
        else:
            df["商品汇总"] = df["商品汇总"].astype(str)
            meals = re.findall(re.compile(r"(.*) \* (\d*)", re.M), df.iloc[0].商品汇总)
            if meals:
                df = Order.Weee_excel_preprocess(df)
            else:
                df = Order.Weee_CSV_preprocess(df)
        Order.CSV2DB(df,restaurant_id,date)
    @classmethod
    def pdf2DB(cls,file_path,restaurant_id,date,is_lunch):
        date += " 12:00" if is_lunch else " 18:00"

        Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date).delete()

        with open(file_path, "rb") as pdf_file:
            text = read_pdf(pdf_file)
            text = "".join(text)
            text = re.split("Order number",text)
            text = text[1:]
            for txt in text:
                meals = fetch_dishes(txt)
                meals_dic = {key:value for key,value in meals}
                Orders.objects.create(idRestaurant_id=restaurant_id,
                                      idDisplay=fetch_id(txt),
                                      Price=fetch_price(txt),ReceiverName=fetch_recipient_name(txt),
                                      Meals=meals_dic,OrderDate=date,DriverId=None,Address=fetch_address(txt),
                                      Phone=fetch_phone_number(txt),
                                      Note=fetch_note(txt))
    @classmethod
    def generate_deliver_list(cls,driver_id, date, isError=False):
        if isError:
            error_order_obj = Orders.objects.filter(DriverId_id__isnull=True,
                                                    isPickup=False,
                                                    idRestaurant__drivers__driverCode=driver_id,
                                                    OrderDate=date + " 18:00").values("ReceiverName", "idDisplay",
                                                                                      "Address", "Phone", "Note",
                                                                                      "Meals").order_by("Sequence")
            if not len(error_order_obj):
                error_order_obj = Orders.objects.filter(DriverId_id__isnull=True,
                                                        isPickup=False,
                                                        idRestaurant__drivers__driverCode=driver_id,
                                                        OrderDate=date + " 12:00").values("ReceiverName", "idDisplay",
                                                                                          "Address", "Phone", "Note",
                                                                                          "Meals").order_by("Sequence")

            # print(error_order_obj)
            error_lst = [{'name': order["ReceiverName"],
                          'orderId': str(order['idDisplay']),
                          'address': order['Address'],
                          'phone': order['Phone'],
                          'note': order['Note'],
                          'dishes': [meal + " X " + str(num) for meal, num in order['Meals'].items()]} for order in
                         error_order_obj]
            return error_lst
        order_obj = Orders.objects.filter(DriverId__driverCode=driver_id,
                                           OrderDate=date+" 18:00").values("ReceiverName","idDisplay","Address","Phone","Note","Meals").order_by("Sequence")
        if not len(order_obj):
            order_obj = Orders.objects.filter(DriverId__driverCode=driver_id,
                                               OrderDate=date + " 12:00").values("ReceiverName","idDisplay","Address","Phone","Note","Meals").order_by("Sequence")
        # print("phone:" ,order_obj[0]['Phone'])
        lst = [{'name':order["ReceiverName"],
                'orderId':str(order['idDisplay']),
                'address':order['Address'],
                'phone':order['Phone'],
                'note':order['Note'],
                'dishes':[meal+" X "+str(num) for meal,num in order['Meals'].items()]} for order in order_obj]
        # obj = Orders.objects.filter(idRestaurant=Restaurant.objects.get(idRestaurant=restaurant_id)
        #                             ,DriverId=driver_id,OrderDate=date).order_by("Sequence")
        # print(obj,type(obj))

        return lst
    @classmethod
    def parser_meals(cls, restaurant_id, date):
        # date += " 12:00" if is_lunch else " 18:00"
        obj = Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date).values("Meals","idDisplay")
        if not len(obj):
            obj = Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date).values("Meals","idDisplay")
        dic = defaultdict(list)
        for meals in obj:
            idOrder = meals['idDisplay']
            for meal,meal_num in meals['Meals'].items():
                for _ in range(int(meal_num)):
                    dic[meal].append(idOrder)
        return dic

    @classmethod
    def assign_order_driver(cls,restaurant_id,date,driver_list,is_lunch):
        date += " 12:00" if is_lunch else " 18:00"
        address = Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date).values("Address","idDisplay","isPickup")
        address_list = []
        pickup_list = []
        for addr in address:
            if addr['isPickup']:
                pickup_list.append(addr['Address'])
            else:
                address_list.append(addr['Address'])
        # address_list = [addr['Address'] for addr in address]
        position,good_addr,err = geocode(address_list)
        cluster_model = EqualGroupsKMeans(n_clusters=len(driver_list),random_state=0)
        cluster_model.fit(position)
        for index,addr in enumerate(good_addr):
            Orders.objects.filter(idRestaurant_id=restaurant_id,
                                  OrderDate=date,
                                  Address=addr.replace("+"," ")).update(DriverId_id = driver_list[cluster_model.labels_[index]])
        for index,addr in enumerate(err):
            Orders.objects.filter(idRestaurant_id=restaurant_id,
                                  OrderDate=date,
                                  Address=addr.replace("+"," ")).update(DriverId_id=None)
    @classmethod
    def generate_sequence(cls,restaurant_id,date,is_lunch):
        date += " 12:00" if is_lunch else " 18:00"
        driver_list_query = Orders.objects.filter(idRestaurant_id=restaurant_id,OrderDate=date).values("DriverId_id").distinct()
        driver_list = [value['DriverId_id'] for value in driver_list_query]
        for driver in driver_list:

            if driver==None:
                continue
            print("generate seq",driver)
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
