from random import choices
from django import forms
import django_filters
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from matplotlib import widgets
from matplotlib.widgets import Widget
from marketplace.models import ProductOrder, Customer, UserShippingAddress
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(help_text='Enter your phone number as +63(phone number), e.g +6391-234-5678')
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields =  ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields =  ['first_name', 'last_name','email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =  ['phone_number','user_image']


class UserShippingAddressFilter(django_filters.FilterSet):
    del_status = [
        ('PENDING', 'PENDING'),
        ('FOR DELIVERY', 'FOR DELIVERY'),
        ('DELIVERED', 'DELIVERED')
    ]

    pay_status = [
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('CANCELLED', 'CANCELLED')
    ]

    transaction_id = django_filters.CharFilter(field_name='order__transaction_id')
    delivery_status = django_filters.ChoiceFilter(field_name='order__delivery_status', choices=del_status)
    payment_status = django_filters.ChoiceFilter(field_name='order__payment_status', choices=pay_status)
    start_date_filter = django_filters.DateFilter(field_name='date_added', lookup_expr='gte')
    end_date_filter = django_filters.DateFilter(field_name='date_added', lookup_expr='lte')

    class Meta:
        model = UserShippingAddress
        fields = '__all__'
        exclude = ['order','home_street','municipality_city','province','country','zip_code', 'date_added']