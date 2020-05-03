"""
Create Date , 
@author: 
"""
from collections import defaultdict
from clustering.equal_groups import EqualGroupsKMeans

from .models import Orders
from accounts.models import Restaurant
from .pdf import *
from .GoogleMap import geocode
class Order:

    @classmethod
    def pdf2DB(cls,file_path,restaurant_id,date):
        # Restaurant.objects.create('')
        # res = Restaurant.objects.get(idRestaurant=restaurant_id)
        res = Restaurant.objects.all()
        print(res)
        with open(file_path, "rb") as pdf_file:
            text = read_pdf(pdf_file)
            text = "".join(text)
            text = text.split("打印订单 - 华⼈⽣鲜第⼀站")
            text = text[1:-1]
            for txt in text:
                meals = fetch_dishes(txt)
                meals_dic = {key:value for key,value in meals}
                Orders.objects.create(idRestaurant=Restaurant.objects.get(idRestaurant=restaurant_id),
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
        print(obj[0])
        dic = defaultdict(list)
        for meals in obj:
            idOrder = meals['idDisplay']
            for meal,meal_num in meals['Meals'].items():
                for _ in range(int(meal_num)):
                    dic[meal].append(idOrder)
        for key,value in dic.items():
            print(key,value)
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
    def generate_sequence(cls,restaurant_id,date,driver_id):
        pass