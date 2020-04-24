"""
Create Date , 
@author: 
"""
class Order:
    def __init__(self,order_id = -1,recipient_name = "", dishes=None,address = "",phone_number = "",note=""):
        self.name = recipient_name
        self.dishes = dishes
        self.address = address
        self.phone = phone_number
        self.order_id = order_id
        self.note = note
    def to_csv_row(self):
        st = ""
        lst = []
        lst+=[self.name,self.order_id,"\""+self.address+"\"",self.phone,self.note]
        lst+=[str(item[0])+" X "+str(item[1]) for item in self.dishes]
        line = ",".join(lst)
        # print(line)
        return line
    def commas_num(self):
        return 4+len(self.dishes)
class OrderList:
    def __init__(self):
        self.list = []
    def to_csv(self,path):
        with open(path,'w',encoding='utf-8') as file:
            commas = []
            for order in self.list:
                commas.append(order.commas_num())
            ma = max(commas)
            file.write("name,id,address,phone,note,dishes"+","*(ma-5)+"\n")
            for index,order in enumerate(self.list):
                file.write(order.to_csv_row()+","*(ma-commas[index])+"\n")
    def add_order(self,order):
        self.list.append(order)
    def sort(self,seq):
        dic = dict()
        for i in range(len(seq)):
            dic[seq[i]] = i
        print(dic)
        self.list = sorted(self.list,key=lambda x:dic[int(x.order_id)])
