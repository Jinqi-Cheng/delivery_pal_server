
from django import forms

from .models import Orders, Drivers
from accounts.models import Restaurant

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['idOrder', 'idRestaurant', 'ReceiverName', 'Price', 'Address','DriverId','Sequence']

class DriverForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(DriverForm, self).__init__(*args, **kwargs)                       
        # self.fields['driverCode'].widget.attrs['disabled'] = 'disabled'
        # self.fields['idRestaurant'].widget.attrs['disabled'] = 'disabled'
        self.fields['driverCode'].widget=forms.HiddenInput()
        self.fields['idRestaurant'].widget=forms.HiddenInput()

    class Meta:
        model = Drivers
        fields = ['driverName','idRestaurant','driverCode']