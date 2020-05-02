"""
Create Date , 
@author: 
"""

from io import StringIO
from io import open
import re

from pdfminer.pdfinterp import process_pdf
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    lines = str(content).split("\n")
    return lines
def fetch_recipient_name(txt):
    recipient_name = re.findall(re.compile(r"Recipient name:(.*)Delivery", re.S), txt)[0]
    return recipient_name
def fetch_address(txt):
    addr = re.findall(re.compile(r"address:(.*), California", re.S), txt)[0]
    return addr
def fetch_phone_number(txt):
    phone_number = re.findall(re.compile(r"phone:(\d*)-*(\d*)-*(\d*)", re.S), txt)[0]
    phone_number = "".join(phone_number)
    return phone_number
def fetch_dishes(txt):
    dishes = re.findall(re.compile(r"phone:[-\d]*(.*)Sub", re.S), txt)
    dishes = dishes[0]
    dishes = re.findall(re.compile(r"([^X]*[^\d])\d+\.\d{2} X (\d{1})\d*\.\d{2}", re.S), dishes)
    print(dishes)
    return dishes
def fetch_id(txt):
    order_id = re.findall(re.compile(r"Order sequence:(\d+)Payment", re.S), txt)[0]
    return order_id
def fetch_note(txt):
    note = re.findall(re.compile(r"Order notes:(.*)Order time", re.S), txt)
    return note[0] if len(note) else ""
def fetch_zip(txt):
    zip = re.findall(re.compile(r"California, (\d{5}), United States",re.S),txt)[0]
    print(zip)
    return zip
def fetch_price(txt):
    price = re.findall(re.compile(r"Amount to be paid(\d*\.\d*)\D", re.S), txt)[0]
    return price

def fetch_pdf(path="",order_list=None):
    with open(path, "rb") as my_pdf:

        text = read_pdf(my_pdf)
        text = "".join(text)
        text = text.split("打印订单 - 华⼈⽣鲜第⼀站")
        text = text[1:-1]
        # for txt in text:
        #     order_list.add_order(Order.Order(
        #         fetch_id(txt),
        #         fetch_recipient_name(txt),
        #         fetch_dishes(txt),
        #         fetch_address(txt),
        #         fetch_phone_number(txt),
        #         fetch_note(txt),
        #         fetch_zip(txt)
        #     ))
            # raise NotImplementedError