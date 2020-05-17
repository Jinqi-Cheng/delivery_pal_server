
from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Orders, Drivers
from accounts.models import Restaurant

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['idOrder', 'idRestaurant', 'ReceiverName', 'Price', 'Address','DriverId','Sequence']

class AddDriverForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(AddDriverForm, self).__init__(*args, **kwargs)                       
        self.fields['driverCode'].widget=forms.HiddenInput()
        self.fields['idRestaurant'].widget=forms.HiddenInput()
    class Meta:
        model = Drivers
        fields = ['driverName','idRestaurant','driverCode']

class ForceDriverPWChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    field_order = ['new_password1', 'new_password2']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.driver)
        return password2
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.driver.set_password(password)
        if commit:
            self.driver.save()
        return self.driver

    def __init__(self, driver,  *args, **kwargs): 
        self.driver = driver
        super().__init__(*args, **kwargs)                       

class DriverPWChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.driver.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.driver)
        return password2
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.driver.set_password(password)
        if commit:
            self.driver.save()
        return self.driver

    def __init__(self, driver,  *args, **kwargs): 
        self.driver = driver
        super().__init__(*args, **kwargs)                       


class MyMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return  "%s | %s" % (obj.driverName, obj.driverCode)
class uploadForm(forms.Form): 
    drivers = MyMultipleModelChoiceField(queryset=Drivers.objects.none(), widget=forms.CheckboxSelectMultiple())
    file = forms.FileField(validators=[ FileExtensionValidator(allowed_extensions=['pdf','csv'])]    \
        ,widget=forms.FileInput(attrs={'accept':'.pdf,.csv'}))
    Period = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}), choices=(('opt1','Lunch'),('opt2','Dinner'),))

    def __init__(self, restaurant_id,*args, **kwargs): 
        super(uploadForm, self).__init__(*args, **kwargs)
        restaurant = Restaurant.objects.get(user_id = restaurant_id)
        self.fields['drivers'].queryset = Drivers.objects.filter(idRestaurant=restaurant)

    def label_from_instance(self, obj):
        return "%s | %s" % (obj.name, obj.field1)