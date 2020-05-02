"""
Create Date , 
@author: 
"""
from collections import defaultdict

from accounts.models import Orders, Restaurant
from .pdf import *
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
                                      idDisp=fetch_id(txt),
                                      Price=fetch_price(txt),ReceiverName=fetch_recipient_name(txt),
                                      Meals=meals_dic,OrderDate=date,DriverId=None,Address=fetch_address(txt))
    @classmethod
    def generate_deliver_list(cls,restaurant_id, driver_id, date):
        obj = Orders.objects.filter(idRestaurant=Restaurant.objects.get(idRestaurant=restaurant_id)
                                    ,DriverId=driver_id,OrderDate=date).order_by("rank")
        print(obj,type(obj))

    @classmethod
    def parser_meals(cls, restaurant_id, date, is_lunch):
        # print("parser")
        obj = Orders.objects.filter(idRestaurant_id=Restaurant.objects.get(idRestaurant=restaurant_id),OrderDate=date).values("Meals","idDisp")
        print(obj[0])
        dic = defaultdict(list)
        for meals in obj:
            idOrder = meals['idDisp']
            for meal,meal_num in meals['Meals'].items():
                for _ in range(int(meal_num)):
                    dic[meal].append(idOrder)
        for key,value in dic.items():
            print(key,value)
        # Orders.objects.filter(idRestaurant=Restaurant.objects.get(idRestaurant=restaurant_id)
        #                       ,OrderDate=date))

    @classmethod
    def x(cls):
        pass