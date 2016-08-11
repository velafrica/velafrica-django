from dal import autocomplete
from velafrica.stock.models import Product, Stock, StockListPosition, StockListPos, Warehouse, StockTransfer
from velafrica.collection.models import Event
from velafrica.organisation.models import Municipality
from django import forms


class WarehouseForm(forms.ModelForm):
    """
    """
    municipality = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:municipality')
    )

    class Meta:
        model = Warehouse
        fields = ('__all__')


class StockForm(forms.ModelForm):
    """
    """
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:product')
    )

    class Meta:
        model = Stock
        fields = ('__all__')


class StockListPosForm(forms.ModelForm):
    """
    """
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:product')
    )

    class Meta:
        model = StockListPos
        fields = ('__all__')


class StockTransferForm(forms.ModelForm):
    """
    """
    warehouse_from = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse')
    )
    warehouse_to = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:warehouse')
    )

    class Meta:
        model = StockTransfer
        fields = ('__all__')


class StockListPositionForm(forms.ModelForm):
    """
    """
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete:product')
    )

    class Meta:
        model = StockListPosition
        fields = ('__all__')
