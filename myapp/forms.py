from django.forms import ModelForm
from django.contrib.auth.models import User, auth
from .models import Transaction
from django import forms
from django.core.validators import RegexValidator

# User/sign up form validation class 
class UserForm(ModelForm):
    username = forms.CharField(required=True, error_messages={'required': 'Please put in a username'})
    first_name = forms.CharField(required=True, error_messages={'required': 'Please put in your first_name'})
    last_name = forms.CharField(required=True, error_messages={'required': 'Please put in your last_name'})
    email = forms.EmailField(required=True, error_messages={'required': 'Email is required'})
    password = forms.CharField(max_length=16, widget=forms.PasswordInput, error_messages={'required': 'Password is required'})
    confirm_password = forms.CharField(max_length=16, widget=forms.PasswordInput, error_messages={'required': 'Confirm Password is required'})
    
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']    
    
    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(UserForm, self).clean()
         
        # extract the username and text field from the data
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
 
        # conditions to be met for the username length
        if password != confirm_password:
            self._errors['password'] = self.error_class([
                'password and confirm pasword do not match'])
        # return any errors if found
        return self.cleaned_data

class TransactionForm(ModelForm):
    name = forms.CharField(required=True, error_messages={'required': 'Please put in an item name'})
    price = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter numbers Only '}))
    # ref = forms.CharField(required=True)
    address = forms.CharField(required=True, error_messages={'required': 'Please fill in your address'})
    phone = forms.CharField(required=True ,error_messages={'incomplete': 'Enter a phone number.'}, 
                               validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')])

    # phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', 
    #                         error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    
    class Meta:
        model = Transaction
        fields = ['name', 'price', 'address', 'phone']    
    
    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(TransactionForm, self).clean()
         
        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        price = self.cleaned_data.get('price')
        # ref = self.cleaned_data.get('ref')
        address = self.cleaned_data.get('address')
        phone = self.cleaned_data.get('phone')
        
 
        # conditions to be met for the username length
        if name == "":
            self._errors['name'] = self.error_class([
                'name is required'])
        if price == 0:
            self._errors['price'] = self.error_class([
                'price should be at least 1'])  
        if address == "":
            self._errors['address'] = self.error_class([
                'address is required'])
        if phone == 0:
            self._errors['phone'] = self.error_class([
                'phone cannot be 0 or have a - or + sign'])
        # return any errors if found
        return self.cleaned_data