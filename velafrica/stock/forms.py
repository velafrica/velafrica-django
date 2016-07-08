from dal import autocomplete
from velafrica.stock.models import Product, Stock, StockListPosition, Warehouse
from velafrica.collection.models import Event
from velafrica.organisation.models import Municipality
from django import forms


class WarehouseForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=autocomplete.ModelSelect2(url='warehouse-autocomplete')
    )

    class Meta:
        model = Warehouse
        fields = ('__all__')

class StockForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='product-autocomplete')
    )

    class Meta:
        model = Stock
        fields = ('__all__')


class StockListPositionForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='product-autocomplete')
    )

    class Meta:
        model = StockListPosition
        fields = ('__all__')