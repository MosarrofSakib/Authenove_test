import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
    #product = django_filters.CharFilter(lookup_expr='exact')
    class Meta:
        model = Order
        fields = ['transaction_id','status',]


class ProductFilter(django_filters.FilterSet):
    #catagory = django_filters.ChoiceFilter(choices= CATAGORY)
    class Meta:
        model = Product
        fields = ['catagory',]