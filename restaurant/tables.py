import django_tables2 as tables
import django_filters
from django_filters.widgets import RangeWidget
from django import forms

from .models import Orders, Drivers

import decimal

class OrderTable(tables.Table):

    Order_Id = tables.Column(accessor='idOrder',verbose_name='ID')
    Price = tables.Column(accessor='Price')
    Receiver_Name = tables.Column(accessor='ReceiverName', verbose_name='Receiver',orderable = True)
    Meals = tables.Column(accessor='Meals')
    Drive_Id = tables.Column(accessor='DriverId__driverName',verbose_name='Driver', orderable = True)
    OrderDate = tables.Column(verbose_name='Date')
    Address = tables.Column(accessor='Address')
    Sequence = tables.Column(accessor='Sequence')
    Phone = tables.Column(accessor='Phone')
    Note = tables.Column(accessor='Note')

    def render_Price(self, value):
        return "${}".format(decimal.Decimal(value).normalize())
    
    class Meta:
        template_name = "django_tables2/semantic.html"


# from django.utils.datastructures import MultiValueDict
from django.http import QueryDict
# from datetime import time
from datetime import datetime, timedelta

class OrderFilter(django_filters.FilterSet):
    # Price__gt = django_filters.NumberFilter(field_name='Price', lookup_expr='gt')
    # Price__lt = django_filters.NumberFilter(field_name='Price', lookup_expr='lt')
    # start = django_filters.DateFromToRangeFilter(field_name="OrderDate",
    datefilter = django_filters.DateFromToRangeFilter(field_name="OrderDate",
        widget=RangeWidget(attrs={'placeholder': 'MM/DD/YYYY', 'type': 'date', 'class': 'datepicker'}),
        )

    def __init__(self, *args, **kwargs):
        if kwargs['data'] is None:
            filter_values = QueryDict(mutable=True)
            today = datetime.today()
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            filter_values['datefilter_min']=start.strftime('%Y-%m-%d')
            filter_values['datefilter_max']=end.strftime("%Y-%m-%d")
            kwargs['data'] = filter_values
            # print(kwargs)
        # else:
        #     filter_values = kwargs['data'].copy()
        #     # print("Have : ", filter_values)

        super().__init__(*args, **kwargs)

    class Meta:
        model = Orders
        fields = ['datefilter','DriverId__driverName']
        # fields = ['Price__gt','Price__lt', 'Driver','datefilter']