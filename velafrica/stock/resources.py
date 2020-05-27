from import_export import resources

from velafrica.stock.models import Product, Warehouse, Stock, StockChange, StockListPosition, StockList, StockTransfer, Category


class ProductResource(resources.ModelResource):
    """
    Define the Product resource for import / export.
    """

    class Meta:
        model = Product
        import_id_fields = ('articlenr',)
        fields = ('category', 'category__name', 'articlenr', 'hscode', 'name', 'name_en', 'name_fr', 'packaging_unit', 'sales_price', 'description')


class WarehouseResource(resources.ModelResource):
    """
    """
    class Meta:
        model = Warehouse


class StockResource(resources.ModelResource):
    """
    Define the Stock resource for import / export.
    """

    class Meta:
        model = Stock
        fields = ('product__articlenr', 'product', 'product__name', 'warehouse', 'warehouse__name', 'amount', 'last_modified')


class StockChangeResource(resources.ModelResource):
    """
    Define the StockChange resource for import / export.
    """

    class Meta:
        model = StockChange


class StockListPositionResource(resources.ModelResource):
    """
    """
    class Meta:
        fields = ['stocklist', 'stocklist__description', 'stocklist__container', 'stocklist__container', 'stocklist__container__partner_to', 'stocklist__container__partner_to__organisation__address__country__name', 'stocklist__container__partner_to__organisation__name', 'product', 'product__name', 'amount']
        model = StockListPosition


class StockListResource(resources.ModelResource):
    """

    """
    class Meta:
        model = StockList


class StockTransferResource(resources.ModelResource):
    """

    """
    class Meta:
        model = StockTransfer


class CategoryResource(resources.ModelResource):
    """
    Define the category resource for import / export.
    """

    class Meta:
        model = Category
        import_id_fields = ('articlenr_start',)
        fields = ('articlenr_start', 'name', 'description')
