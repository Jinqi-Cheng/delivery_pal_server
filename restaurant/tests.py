from django.test import TestCase
from .Order import Order
# Create your tests here.
class OrderTestCases(TestCase):
    # def setUp(self):
    #     pass
    def test_pdf2DB(self):
        Order.pdf2DB("./miscellaneous/4.30 92129.pdf",1,"05/01/2020")
        # s