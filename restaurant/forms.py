
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
        self.fields['driverCode'].widget=forms.HiddenInput()
        self.fields['idRestaurant'].widget=forms.HiddenInput()
        self.fields['driverName'].widget= forms.TextInput(attrs={'class':'form-control','placeholder':'请在此输入司机名称'})
    class Meta:
        model = Drivers
        fields = ['driverName','idRestaurant','driverCode']

class MyMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return  "%s | %s" % (obj.driverName, obj.driverCode)
class uploadForm(forms.Form): 
    drivers = MyMultipleModelChoiceField(queryset=Drivers.objects.none(), widget=forms.CheckboxSelectMultiple(attrs={'class':'upload_multi_choice'}),
                                         label='骑手')
    file = forms.FileField(validators=[ FileExtensionValidator(allowed_extensions=['pdf','csv'])]    \
        ,widget=forms.FileInput(attrs={'accept':'.pdf,.csv','class':'html_file_upload'}),label='文件')
    # Period = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}),
    #                            choices=(('opt1','Lunch'),('opt2','Dinner'),),label='送餐时间')
    Period = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'form-control col-6'}),
                               choices=(('opt1', '午餐'), ('opt2', '晚餐'),), label='送餐时间')
    order_options = forms.ChoiceField(required=True,widget=forms.Select(attrs={'class': 'form-control col-6'}),
                               choices=(('opt1', '自动排序'), ('opt2', '按Zipcode排序'),), label='排序方式')
    def __init__(self, restaurant_id,*args, **kwargs):
        super(uploadForm, self).__init__(*args, **kwargs)
        restaurant = Restaurant.objects.get(user_id = restaurant_id)
        self.fields['drivers'].queryset = Drivers.objects.filter(idRestaurant=restaurant)

    def label_from_instance(self, obj):
        return "%s | %s" % (obj.name, obj.field1)
    
class ManageAddress(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={'id':'address_form'}))