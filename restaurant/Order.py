"""
Create Date , 
@author: 
"""
from accounts.models import Orders, Restaurant
from .pdf import *
class Order:

    @classmethod
    def pdf2DB(cls,file_path,restaurant_id,date):
        # Restaurant.objects.create('')
        res = Restaurant.objects.all()
        print(res)
        with open(file_path, "rb") as pdf_file:
            text = read_pdf(pdf_file)
            text = "".join(text)
            text = text.split("打印订单 - 华⼈⽣鲜第⼀站")
            text = text[1:-1]
            for txt in text:
                meals = fetch_dishes(txt)
                # Orders.objects.create(idRestaurant=Restaurant.objects.get(idRestaurant=restaurant_id)
                #                       ,Price=fetch_price(txt),ReceiverName=fetch_recipient_name(txt),Meals="",OrderDate=date,DriverId=None,Address=fetch_address(txt))
    @classmethod
    def generate_deliver_list(cls,restaurant_id, driver_id, date):
        obj = Orders.objects.filter(idRestaurant=Restaurant.objects.get(idRestaurant=restaurant_id)
                                    ,DriverId=driver_id,OrderDate=date).order_by("rank")
        print(obj,type(obj))

    @classmethod
    def parser_meals(cls, restaurant_id, date, is_lunch):
        pass

    @classmethod
    def x(cls):
        pass