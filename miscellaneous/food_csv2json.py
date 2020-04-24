"""
Create Date , 
@author: 
"""

import json

dishes_table = {
"农家小炒肉（购满39.9加购） x 1":"农家小炒肉",
    "农家小炒肉 x 1":"农家小炒肉",
"美美嫩豆腐（盒）订餐客人专享 x 1" : "美美嫩豆腐",
"皮蛋擂茄子 x 1" : "皮蛋擂茄子",
"新鲜大白菜（颗）订餐客人专享 x 1" : "新鲜大白菜",
"爆炒牛蛙 x 1":"爆炒牛蛙",
    "梅菜扣肉（不辣） x 1":"梅菜扣肉",
    "酸菜椒香鱼片 x 1":"酸菜椒香鱼片",
    "糖醋排骨（小朋友的最爱） x 1":"糖醋排骨",
    "馋嘴卤粉 x 1":"馋嘴卤粉",
    "石锅羊肉（不辣） x 1":"石锅羊肉",
    "石锅牛肉（不辣） x 1":"石锅牛肉",
    "干锅烟笋腊肉 x 1":"干锅烟笋腊肉",
    "香煎平锅黄鱼（不辣） x 1":"香煎平锅黄鱼",
    "湖南粉蒸肉 x 1":"湖南粉蒸肉",
    "萝卜干炒腊肉 x 1":"萝卜干炒腊肉",
    "干锅坛子辣椒炒鸡 x 1":"干锅坛子辣椒炒鸡",
    "桂花盐水鸭（不辣）零食首选 x 1":"桂花盐水鸭",
    "红糖糍粑 x 1":"红糖糍粑",
    "米饭 x 1":"米饭",
    "牙签羊肉 x 1":"牙签羊肉",
    "农家煎豆腐（不辣） x 1":"农家煎豆腐",
    "莲藕排骨汤 x 1":"莲藕排骨汤",
    "养生药膳猪肚鸡（不辣） x 1":"养生药膳猪肚鸡",
    "养生土鸡汤 x 1":"养生土鸡汤",
    "脖子猪肚 x 1":"脖子猪肚",
    "清炒莴笋片（不辣） x 1":"清炒莴笋片",
    "酸辣鸡杂 x 1":"酸辣鸡杂",
    "香辣烤鱼 x 1":"香辣烤鱼",
    "毛氏红烧肉 x 1":"毛氏红烧肉",
    "柴火香干（不辣） x 1":"柴火香干",
    "食神牛腩 x 1":"食神牛腩",
    "雪里蕻肉沫 x 1":"雪里蕻肉沫",
    "野山椒牛肉 x 1":"野山椒牛肉",
    "南瓜饼 x 1":"南瓜饼",
    "银耳羹 菜金满39.99加购（不含豆腐） x 1":"银耳羹",
    "风吹黄瓜皮 x 1":"风吹黄瓜皮",
    "麻婆豆腐 x 1":"麻婆豆腐"

}
# with open("../../../2020送餐/daily_order.csv",'r',encoding='utf-8') as file:
with open("tmp.csv",'r',encoding='utf-8') as file:
    file.readline()
    lines = file.readlines()
    lst = []
    for line in lines:
        print(line)
        dic = dict()
        # print(line)
        field = line.split(",")
        field = [i for i in field if i!='\n']
        name = field[0]
        id = field[1]
        address = field[2]+","+field[3]
        phone = field[4]
        # print(phone)
        note = field[5]
        dishes = field[6:]
        dishes = [i for i in dishes if i]
        dishes_T = []
        for dish in dishes:
            if dish in dishes_table:
                dishes_T.append(dishes_table[dish])
            else:
                dishes_T.append(dish)
        dic = {'name':name,'orderId':id,'address':address,'phone':phone,'note':note,'dishes':dishes_T}
        lst.append(dic)
    print(lst)
    js = json.dumps(lst,indent=4).encode('utf-8')
    with open("./static/daily_order.json",'w',encoding='utf-8') as file_w:
        file_w.write(str(lst).replace("\"","").replace("\'","\""))

    # print(js)
# print(df)