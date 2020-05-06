
from django import forms
from django.core.validators import FileExtensionValidator

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
class MyMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return  "%s | %s" % (obj.driverName, obj.driverCode)
class uploadForm(forms.Form): 
    drivers = MyMultipleModelChoiceField(queryset=Drivers.objects.none(), widget=forms.CheckboxSelectMultiple())
    file = forms.FileField(validators=[ FileExtensionValidator(allowed_extensions=['pdf'])]    \
        ,widget=forms.FileInput(attrs={'accept':'.pdf'}))
    Period = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}), choices=(('opt1','Lunch'),('opt2','Dinner'),))

    def __init__(self, restaurant_id,*args, **kwargs): 
        super(uploadForm, self).__init__(*args, **kwargs)
        restaurant = Restaurant.objects.get(user_id = restaurant_id)
        self.fields['drivers'].queryset = Drivers.objects.filter(idRestaurant=restaurant)

    def label_from_instance(self, obj):
        return "%s | %s" % (obj.name, obj.field1)